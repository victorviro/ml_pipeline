import logging.config

from fastapi import status  # starlette statuses
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.logging_config import LOGGING_CONFIG
from src.transform_data.application.fit_transformer_use_case import FitTransformer

from .mlflow_transformer_tracker import MlflowTransformerTracker
from .sklearn_transformation_fitter import SklearnTransformationFitter

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class FitItem(BaseModel):
    data_path: str
    data_name: str
    size_test_split: float
    test_split_seed: int
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/fit_transformer_pipeline")
async def fit_transformer_pipeline_endpoint(item: FitItem):
    json_data_loader = JSONDataLoader()
    sklearn_transformation_fitter = SklearnTransformationFitter(
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed
    )
    mlflow_transformer_tracker = MlflowTransformerTracker(run_id=item.mlflow_run_id)

    fit_transformer_use_case = FitTransformer(
        data_file_loader=json_data_loader,
        transformation_fitter=sklearn_transformation_fitter,
        data_tracker=mlflow_transformer_tracker
    )
    data_file_path = f'{item.data_path}/{item.data_name}.json'
    logger.info('Fitting and tracking data transfomer...')
    try:
        fit_transformer_use_case.execute(dataset_file_path=data_file_path)
        message = 'Transformer pipeline fitted and tracked succesfully.'
        logger.info(message)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error fitting or tracking transformer pipeline: {str(err)}.'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.transform_data.infrastructure.transform_data_api_controller:rest_api --port
# 1215
