import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.version_data.application.version_data_use_case import VersionData
from .dvc_data_versioner import DVCDataVersioner


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str
    data_version: float
    git_remote_name: str
    git_branch_name: str


rest_api = FastAPI()


@rest_api.post("/api/version_data")
async def version_data_endpoint(item: Item):
    dvc_data_versioner = DVCDataVersioner(git_remote_name=item.git_remote_name,
                                          git_branch_name=item.git_branch_name)
    data_file_path = f"{item.data_path}/{item.data_name}.json"

    version_data_use_case = VersionData.build(data_versioner=dvc_data_versioner)

    try:
        version_data_use_case.execute(
            data_file_path=data_file_path,
            data_version=item.data_version
        )
        message = 'Data versioned succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error versioning the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.version_data.infrastructure.version_data_api_controller:rest_api --port 1217
