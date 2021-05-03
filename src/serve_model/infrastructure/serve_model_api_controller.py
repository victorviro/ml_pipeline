import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.serve_model.application.serve_model_use_case import ServeModel
from src.shared.infrastructure.mlflow_api_tracker import MlflowApiTracker
from .gcp_model_server import GCPModelServer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/served_model")
async def serve_model_endpoint(item: Item):
    gcp_model_server = GCPModelServer()
    mlflow_api_tracker = MlflowApiTracker(run_id=item.mlflow_run_id)
    artifacts_path = mlflow_api_tracker.get_artifacts_path()
    model_version = mlflow_api_tracker.search_model_version()
    version_name = f'v{model_version}'

    serve_model_use_case = ServeModel.build(
        model_server=gcp_model_server,
        data_tracker=mlflow_api_tracker
    )
    model_gcs_path = f'{artifacts_path}/'

    try:
        logger.info('Making predictions...')
        serve_model_use_case.execute(
            model_file_path=model_gcs_path,
            version_name=version_name
        )
        message = 'Model served succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error serving the model: {str(err)}'
        logger.error(message)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.serve_model.infrastructure.serve_model_api_controller:rest_api --port 1219
