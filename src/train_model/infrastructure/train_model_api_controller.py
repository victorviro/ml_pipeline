import logging.config

from fastapi import status  # starlette statuses
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.constants import REGISTRY_MODEL_NAME, TRANSFORMER_PIPELINE_NAME
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.infrastructure.mlflow_model_register import MlflowModelRegister
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker
from src.shared.logging_config import LOGGING_CONFIG
from src.train_model.application.train_model_use_case import TrainModel
from src.train_model.infrastructure.sklearn_model_trainer import SklearnModelTrainer

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    data_name: str
    alpha: float
    l1_ratio: float
    size_test_split: float
    test_split_seed: int
    model_seed: int
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/train_model")
def train_model_endpoint(item: Item):
    model_trainer = SklearnModelTrainer(
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed,
        alpha=item.alpha,
        l1_ratio=item.l1_ratio,
        model_seed=item.model_seed,
    )
    dataset_file_loader = JSONDataLoader()
    data_tracker = MlflowPythonTracker(run_id=item.mlflow_run_id)
    model_register = MlflowModelRegister(run_id=item.mlflow_run_id)

    train_model_use_case = TrainModel.build(
        model_trainer=model_trainer,
        dataset_file_loader=dataset_file_loader,
        data_tracker=data_tracker,
        model_register=model_register,
        registry_model_name=REGISTRY_MODEL_NAME,
        data_preprocessor_name=TRANSFORMER_PIPELINE_NAME,
    )
    dataset_file_path = f"{item.raw_data_path}/{item.data_name}.json"

    logger.info("Train the model and track it...")
    try:
        train_model_use_case.execute(dataset_file_path=dataset_file_path)
        message = "Model trained and metadata tracked succesfully"
        logger.info(message)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": message}
        )
    except Exception as err:
        message = f"Error training the model or tracking metadata: {str(err)}"
        logger.error(message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": message},
        )


# uvicorn src.train_model.infrastructure.train_model_api_controller:rest_api --port 1216
