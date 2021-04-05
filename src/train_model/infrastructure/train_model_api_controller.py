import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.train_model.application.train_model_use_case import TrainModel
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker
from.mlflow_sklearn_trainer import MlflowSklearnTrainer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    data_name: str
    alpha: float
    l1_ratio: float
    transformer_name: str
    model_name: str
    size_test_split: float
    test_split_seed: int
    model_seed: int
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/train_model")
async def train_model_endpoint(item: Item):
    mlflow_sklearn_trainer = MlflowSklearnTrainer(
        transformer_name=item.transformer_name, size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed, alpha=item.alpha, l1_ratio=item.l1_ratio,
        model_seed=item.model_seed, model_name=item.model_name
    )
    json_data_loader = JSONDataLoader()
    mlflow_python_tracker = MlflowPythonTracker(run_id=item.mlflow_run_id)

    train_model_use_case = TrainModel.build(
        model_trainer=mlflow_sklearn_trainer,
        data_file_loader=json_data_loader,
        data_tracker=mlflow_python_tracker
    )
    data_file_path = f'{item.raw_data_path}/{item.data_name}.json'

    logger.info('Train the model...')
    try:
        train_model_use_case.execute(data_file_path=data_file_path)
        message = 'Model trained and info tracked succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error training the model or tracking info: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.train_model.infrastructure.train_model_api_controller:rest_api --port 1216
