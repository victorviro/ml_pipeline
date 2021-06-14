import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.validate_model.application.validate_model_use_case import ValidateModel
from .mlflow_model_validation_tracker import MlflowModelValidationTracker

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    rmse_threshold: float
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/validate_model")
async def train_model_endpoint(item: Item):
    mlflow_model_validation_tracker = MlflowModelValidationTracker(
        run_id=item.mlflow_run_id
    )
    validate_model_use_case = ValidateModel.build(
        data_tracker=mlflow_model_validation_tracker
    )
    metrics_threshold = {
        "rmse": item.rmse_threshold
    }
    try:
        logger.info(f'Validating model...')
        validate_model_use_case.execute(metrics_threshold=metrics_threshold)
        message = 'Model validated succesfully.'
        logger.info(message)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the model: {str(err)}.'
        logger.error(message)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.validate_model.infrastructure.validate_model_api_controller:rest_api --port
# 1218
