import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.train_model.application.train_model_use_case import train_model
from.mlflow_sklearn_trainer import MlflowSklearnTrainer


logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    transformed_data_path: str
    data_name: str
    alpha: float
    l1_ratio: float


rest_api = FastAPI()


@rest_api.post("/api/train_model")
async def train_model_endpoint(item: Item):
    mlflow_sklearn_trainer = MlflowSklearnTrainer(
        raw_data_path=item.raw_data_path,
        transformed_data_path=item.transformed_data_path,
        data_name=item.data_name,
        alpha=item.alpha,
        l1_ratio=item.l1_ratio
    )

    try:
        artifact_uri = train_model(mlflow_sklearn_trainer)
        return {'message': 'succes', 'artifact_uri': artifact_uri}  # 200
    except Exception as err:
        return {'message': str(err)}  # 400

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.train_model.infrastructure.mlflow_sklearn_trainer_api:rest_api
# --port 1216
