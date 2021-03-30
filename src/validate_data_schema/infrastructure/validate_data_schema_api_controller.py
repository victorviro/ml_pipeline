import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.validate_data_schema.application.validate_data_schema_use_case import (
    ValidateDataSchema)
from .pandera_schema_validator import PanderaSchemaValidator, MCPL_SCHEMA
from src.shared.infrastructure.json_data_loader import JSONDataLoader


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/validate_data_schema")
async def validate_data_schema_endpoint(item: Item):
    data_file_loader = JSONDataLoader()
    data_validator = PanderaSchemaValidator()
    file_path = f"{item.data_path}/{item.data_name}.json"

    validate_data_schema = ValidateDataSchema.build(
        data_file_loader=data_file_loader,
        data_validator=data_validator
    )

    try:
        # Load the data and validate its schema
        validate_data_schema.execute(file_path=file_path, data_schema=MCPL_SCHEMA)
        message = 'Data schema validated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the schema of the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.validate_data_schema.infrastructure.validate_data_schema_api_controller:
# rest_api --port 1214