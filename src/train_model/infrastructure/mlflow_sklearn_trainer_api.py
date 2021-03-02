import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.logging_config import LOGGING_CONFIG
from src.train_model.application.train_model_use_case import train_model
from.mlflow_sklearn_trainer import MlflowSklearnTrainer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    transformed_data_path: str
    data_name: str
    alpha: float
    l1_ratio: float
    version: int
    model_path: str
    model_name: str
    size_test_split: float
    test_split_seed: int
    model_seed: int


rest_api = FastAPI()


@rest_api.post("/api/train_model")
async def train_model_endpoint(item: Item):
    mlflow_sklearn_trainer = MlflowSklearnTrainer(
        raw_data_path=item.raw_data_path,
        transformed_data_path=item.transformed_data_path,
        data_name=item.data_name,
        alpha=item.alpha,
        l1_ratio=item.l1_ratio,
        version=item.version,
        model_path=item.model_path,
        model_name=item.model_name,
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed,
        model_seed=item.model_seed
    )

    try:
        train_model(mlflow_sklearn_trainer)
        message = 'Model trained succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error training the model: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.train_model.infrastructure.mlflow_sklearn_trainer_api:rest_api --port 1216
