import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.validate_model.application.validate_model_use_case import ValidateModel
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
    sklearn_model_validator = SklearnModelValidator()
    json_data_loader = JSONDataLoader()

    validate_model_use_case = ValidateModel.build(
        model_validator=sklearn_model_validator,
        data_file_loader=json_data_loader
    )
    data_file_path = f'{item.raw_data_path}/{item.data_name}.json'

    try:
        validate_model_use_case.execute(
            data_file_path=data_file_path, rmse_threshold=item.rmse_threshold,
            size_test_split=item.size_test_split, test_split_seed=item.test_split_seed
        )
        message = 'Model validated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the model: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.validate_model.infrastructure.validate_model_api_controller:rest_api --port
# 1218
