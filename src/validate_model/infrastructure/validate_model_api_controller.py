import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.shared.constants import MODEL_NAME, TRANSFORMER_PIPELINE_NAME
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.validate_model.application.validate_model_use_case import ValidateModel
from src.shared.infrastructure.pickle_data_loader import PickleDataLoader
from .sklearn_model_validator import SklearnModelValidator
from .mlflow_model_validation_tracker import MlflowModelValidationTracker

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    data_name: str
    size_test_split: float
    test_split_seed: int
    rmse_threshold: float
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/validate_model")
async def train_model_endpoint(item: Item):
    sklearn_model_validator = SklearnModelValidator(
        rmse_threshold=item.rmse_threshold,
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed
    )
    json_data_loader = JSONDataLoader()
    pickle_data_loader = PickleDataLoader()
    mlflow_api_tracker = MlflowModelValidationTracker(run_id=item.mlflow_run_id)
    artifacts_path = mlflow_api_tracker.get_artifacts_path()

    validate_model_use_case = ValidateModel.build(
        model_validator=sklearn_model_validator,
        dataset_file_loader=json_data_loader,
        model_file_loader=pickle_data_loader,
        data_tracker=mlflow_api_tracker
    )
    data_file_path = f'{item.raw_data_path}/{item.data_name}.json'
    model_path = f'{artifacts_path}/{MODEL_NAME}.pkl'
    transformer_path = f'{artifacts_path}/{TRANSFORMER_PIPELINE_NAME}.pkl'

    try:
        logger.info(f'Validating model...')
        validate_model_use_case.execute(
            data_file_path=data_file_path,
            model_path=model_path,
            transformer_path=transformer_path
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
