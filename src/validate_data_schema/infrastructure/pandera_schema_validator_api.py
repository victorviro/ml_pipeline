import logging

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.validate_data_schema.application.validate_data_schema_use_case import (
    validate_schema)
from .pandera_schema_validator import PanderaSchemaValidator


logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/validate_data_schema")
async def validate_data_schema_endpoint(item: Item):
    pandera_schema_validator = PanderaSchemaValidator(
        data_path=item.data_path,
        data_name=item.data_name
    )

    try:
        validate_schema(pandera_schema_validator)
        message = 'Data schema validated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the schema of the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.validate_data_schema.infrastructure.pandera_schema_validator_api:rest_api
# --port 1214
