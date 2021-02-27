import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.transform_data.application.transform_data_use_case import transform_data
from.sklearn_data_transformer import SklearnDataTransformer


logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str
    data_output_path: str


rest_api = FastAPI()


@rest_api.post("/api/transform_data")
async def transform_data_endpoint(item: Item):
    sklearn_data_transformer = SklearnDataTransformer(
        data_path=item.data_path,
        data_name=item.data_name,
        data_output_path=item.data_output_path
    )

    try:
        transform_data(sklearn_data_transformer)
        return {'message': 'succes'}  # 200
    except Exception as err:
        return {'message': str(err)}  # 400

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.transform_data.infrastructure.sklearn_data_transformer_api:rest_api
# --port 1215
