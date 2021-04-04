import logging.config
import os

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.shared.infrastructure.mlflow_api_tracker import MlflowApiTracker
from src.version_data.application.version_data_use_case import VersionTrackData
from src.shared.constants import MLFLOW_API_URI, MLFLOW_API_ENDPOINT_LOG_BATCH
from .dvc_data_versioner import DVCDataVersioner


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str
    data_version: float
    git_remote_name: str
    git_branch_name: str
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/version_data")
async def version_data_endpoint(item: Item):
    dvc_data_versioner = DVCDataVersioner(git_remote_name=item.git_remote_name,
                                          git_branch_name=item.git_branch_name)
    data_file_path = f"{item.data_path}/{item.data_name}.json"
    mlflow_api_tracker = MlflowApiTracker(
        run_id=item.mlflow_run_id,
        key='tags',
        url=f'{MLFLOW_API_URI}/{MLFLOW_API_ENDPOINT_LOG_BATCH}'
    )

    version_data_use_case = VersionTrackData.build(data_versioner=dvc_data_versioner,
                                                   data_tracker=mlflow_api_tracker)

    try:
        version_data_use_case.execute(
            data_file_path=data_file_path,
            data_version=item.data_version
        )
        message = 'Data versioned and tracked succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error versioning the dataset or tracking data information: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.version_data.infrastructure.version_data_api_controller:rest_api --port 1217
