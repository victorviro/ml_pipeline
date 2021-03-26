import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.transform_data.application.transform_data_use_case import transform_data
from.sklearn_data_transformer import SklearnDataTransformer, SklearnFitDataTransformer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class FitItem(BaseModel):
    data_path: str
    data_name: str
    transformer_pipe_path: str
    pipe_name: str
    size_test_split: float
    test_split_seed: int


rest_api = FastAPI()


@rest_api.post("/api/fit_transformer_pipeline")
async def fit_transformer_pipeline_endpoint(item: FitItem):
    sklearn_fit_data_transformer = SklearnFitDataTransformer(
        data_path=item.data_path,
        data_name=item.data_name,
        transformer_pipe_path=item.transformer_pipe_path,
        pipe_name=item.pipe_name,
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed
    )
    logger.info(f'Transforming training raw data. Name: {item.data_name}')

    try:
        sklearn_fit_data_transformer.fit_transfomer_pipeline()
        sklearn_fit_data_transformer.save_transformer_pipeline()
        message = 'Transformer pipeline fitted succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error fitting transformer pipeline: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})


class TransformItem(BaseModel):
    data: dict
    transformer_pipe_path: str
    pipe_name: str


@rest_api.post("/api/transform_data")
async def transform_data_endpoint(item: TransformItem):
    sklearn_data_transformer = SklearnDataTransformer(
        transformer_pipe_path=item.transformer_pipe_path,
        pipe_name=item.pipe_name
    )
    logger.info(f'Transforming serving raw data')
    try:
        transformed_data = transform_data(sklearn_data_transformer, item.data)
        message = 'Data transformed succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message, 'data': transformed_data})
    except Exception as err:
        message = f'Error transforming the data: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.transform_data.infrastructure.sklearn_data_transformer_api:rest_api --port
# 1215
