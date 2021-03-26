import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.validate_model.application.validate_model_use_case import validate_model
from.sklearn_model_validator import SklearnModelValidator


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    data_name: str
    size_test_split: float
    test_split_seed: int
    rmse_threshold: float


rest_api = FastAPI()


@rest_api.post("/api/validate_model")
async def train_model_endpoint(item: Item):
    sklearn_model_validator = SklearnModelValidator(
        raw_data_path=item.raw_data_path,
        data_name=item.data_name,
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed,
        rmse_threshold=item.rmse_threshold
    )

    try:
        validate_model(sklearn_model_validator)
        message = 'Model validated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the model: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.validate_model.infrastructure.sklearn_model_validator_api:rest_api --port
# 1218
