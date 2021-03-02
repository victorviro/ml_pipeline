import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.logging_config import LOGGING_CONFIG
from src.version_data.application.version_data_use_case import version_data
from .dvc_data_versioner import DVCDataVersioner


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    relative_data_path: str
    data_name: str
    data_version: int
    git_remote_name: str
    git_branch_name: str


rest_api = FastAPI()


@rest_api.post("/api/version_data")
async def version_data_endpoint(item: Item):
    dvc_data_versioner = DVCDataVersioner(
        relative_data_path=item.relative_data_path,
        data_name=item.data_name,
        data_version=item.data_version,
        git_remote_name=item.git_remote_name,
        git_branch_name=item.git_branch_name
    )

    try:
        version_data(dvc_data_versioner)
        message = 'Data versioned succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error versioning the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.version_data.infrastructure.dvc_data_versioner_api:rest_api --port 1217
