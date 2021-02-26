import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.validate_data_schema.application.validate_data_schema_use_case import (
    validate_schema)
from .pandera_schema_validator import PanderaSchemaValidator


logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/validate_data_schema_endpoint")
async def root(item: Item):
    pandera_schema_validator = PanderaSchemaValidator(
        data_path=item.data_path,
        data_name=item.data_name
    )

    try:
        validate_schema(pandera_schema_validator)
        return {'message': 'succes'}  # 200
    except Exception as err:
        return {'message': str(err)}  # 400

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.validate_data_schema.infrastructure.pandera_schema_validator_api:rest_api
# --port 1214
