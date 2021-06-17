import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.version_data.infrastructure.mlflow_data_versioning_tracker import (
    MlflowDataVersioningTracker)
from src.version_data.application.version_data_use_case import VersionTrackData
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
    mlflow_data_versioning_tracker = MlflowDataVersioningTracker(
        run_id=item.mlflow_run_id
    )

    version_data_use_case = VersionTrackData.build(
        data_versioner=dvc_data_versioner,
        data_tracker=mlflow_data_versioning_tracker
    )

    try:
        logger.info('Versioning the dataset...')
        version_data_use_case.execute(
            data_file_path=data_file_path,
            data_version=item.data_version
        )
        message = 'Data versioned and tracked succesfully'
        logger.info(message)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error versioning the dataset or tracking data information: {str(err)}'
        logger.error(message)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.version_data.infrastructure.version_data_api_controller:rest_api --port 1217
