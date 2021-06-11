import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.validate_data_schema.application.validate_data_schema_use_case import (
    ValidateDataSchema)
from .pandera_schema_validator import PanderaSchemaValidator
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.constants import DATASET_SCHEMA_FILENAME


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/validate_data_schema")
async def validate_data_schema_endpoint(item: Item):
    json_data_loader = JSONDataLoader()
    pandera_schema_validator = PanderaSchemaValidator()
    dataset_file_path = f"{item.data_path}/{item.data_name}.json"
    dataset_schema_info_file_path = f"{item.data_path}/{DATASET_SCHEMA_FILENAME}.json"

    validate_data_schema = ValidateDataSchema.build(
        data_validator=pandera_schema_validator,
        dataset_file_loader=json_data_loader,
        dataset_schema_info_file_loader=json_data_loader
    )

    try:
        # Load the data and validate its schema
        validate_data_schema.execute(
            dataset_file_path=dataset_file_path,
            dataset_schema_info_file_path=dataset_schema_info_file_path
        )
        message = 'Data schema validated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error validating the schema of the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.validate_data_schema.infrastructure.validate_data_schema_api_controller:
# rest_api --port 1214
