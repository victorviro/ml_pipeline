import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.transform_data.application.transform_data_use_case import TransformData
from src.transform_data.application.fit_transformer_use_case import FitTransformer
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.infrastructure.pickle_data_loader import PickleDataLoader
from src.shared.infrastructure.pickle_data_saver import PickleDataSaver
from .sklearn_data_transformer import SklearnDataTransformer
from .sklearn_transformation_fitter import SklearnTransformationFitter
from .mlflow_artifact_tracker import MlflowArtifactTracker


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class FitItem(BaseModel):
    data_path: str
    data_name: str
    transformer_pipe_path: str
    pipe_name: str
    size_test_split: float
    test_split_seed: int
    model_name: str
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/fit_transformer_pipeline")
async def fit_transformer_pipeline_endpoint(item: FitItem):
    json_data_loader = JSONDataLoader()
    sklearn_transformation_fitter = SklearnTransformationFitter(
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed
    )
    pickle_data_saver = PickleDataSaver()
    transformer_file_path = f'{item.transformer_pipe_path}/{item.pipe_name}.pkl'
    data_file_path = f'{item.data_path}/{item.data_name}.json'

    mlflow_artifact_tracker = MlflowArtifactTracker(
        run_id=item.mlflow_run_id,
        model_name=item.model_name)

    fit_transformer_use_case = FitTransformer(
        data_file_loader=json_data_loader,
        transformation_fitter=sklearn_transformation_fitter,
        data_file_saver=pickle_data_saver,
        data_tracker=mlflow_artifact_tracker
    )

    logger.info('Fitting transfomer...')

    try:
        fit_transformer_use_case.execute(
            data_file_path=data_file_path,
            transformer_file_path=transformer_file_path
        )
        message = 'Transformer pipeline fitted and tracked succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error fitting or tracking transformer pipeline: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})


class TransformItem(BaseModel):
    data: dict
    transformer_pipe_path: str
    pipe_name: str


@rest_api.post("/api/transform_data")
async def transform_data_endpoint(item: TransformItem):
    transformer_file_path = f'{item.transformer_pipe_path}/{item.pipe_name}.pkl'
    sklearn_data_transformer = SklearnDataTransformer(
        transformer_file_path=transformer_file_path
    )
    pickle_data_loader = PickleDataLoader()

    transform_data_use_case = TransformData.build(
        data_transformer=sklearn_data_transformer,
        data_file_loader=pickle_data_loader
    )
    logger.info(f'Transforming data')
    try:
        # Transform the dataset
        transformed_data = transform_data_use_case.execute(data=item.data)
        message = 'Data transformed succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message, 'data': transformed_data})
    except Exception as err:
        message = f'Error transforming the data: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.transform_data.infrastructure.transform_data_api_controller:rest_api --port
# 1215
