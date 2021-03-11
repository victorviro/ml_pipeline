import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.shared.files_helper import load_pickle_file
from src.transform_data.application.transform_data_use_case import transform_data
from.sklearn_data_transformer import SklearnDataTransformer, SklearnTrainDataTransformer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str
    data_output_path: str
    model_path: str
    pipe_name: str


rest_api = FastAPI()


@rest_api.post("/api/transform_train_data")
async def transform_train_data_endpoint(item: Item):
    sklearn_train_data_transformer = SklearnTrainDataTransformer(
        data_path=item.data_path,
        data_name=item.data_name,
        data_output_path=item.data_output_path,
        model_path=item.model_path,
        pipe_name=item.pipe_name
    )
    logger.info(f'Transforming training raw data. Name: {item.data_name}')

    try:
        raw_data = sklearn_train_data_transformer.get_data()
        mcpl = raw_data.pop('max_char_per_line', None)
        transformer_pipeline = sklearn_train_data_transformer.fit_transfomer_pipeline(
            raw_data
        )
        sklearn_train_data_transformer.save_transformer_pipeline(transformer_pipeline)
        transformed_data = transform_data(sklearn_train_data_transformer,
                                          raw_data, transformer_pipeline)
        transformed_data.update({'max_char_per_line': mcpl})
        sklearn_train_data_transformer.save_data(transformed_data)
        message = 'Training data transformed succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error transforming the training data: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})


class ServingItem(BaseModel):
    font_size: int
    rows_number: int
    cols_number: int
    char_number_text: int
    model_path: str
    pipe_name: str


@rest_api.post("/api/transform_serving_data")
async def transform_serving_data_endpoint(item: ServingItem):
    raw_data = {
        "font_size": [item.font_size],
        "rows_number": [item.rows_number],
        "cols_number": [item.cols_number],
        "char_number_text": [item.char_number_text]
    }
    sklearn_data_transformer = SklearnDataTransformer()
    logger.info(f'Transforming serving raw data')

    try:
        transformer_pipeline = load_pickle_file(f'{item.model_path}/{item.pipe_name}.pkl')
        transformed_data = transform_data(sklearn_data_transformer,
                                          raw_data, transformer_pipeline)
        message = 'Serving data transformed succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message, 'data': transformed_data})
    except Exception as err:
        message = f'Error transforming the serving data: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.transform_data.infrastructure.sklearn_data_transformer_api:rest_api --port
# 1215
