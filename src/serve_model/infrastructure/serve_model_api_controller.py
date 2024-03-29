import logging.config

from fastapi import status  # starlette statuses
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.serve_model.application.serve_model_use_case import ServeModel
from src.serve_model.infrastructure.gcp_model_server import GCPModelServer
from src.shared.constants import MODEL_VERSION
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker
from src.shared.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/served_model")
async def serve_model_endpoint(item: Item) -> JSONResponse:
    model_server = GCPModelServer()
    data_tracker = MlflowPythonTracker(run_id=item.mlflow_run_id)

    serve_model_use_case = ServeModel.build(
        model_server=model_server,
        data_tracker=data_tracker,
        model_version=MODEL_VERSION,
    )

    try:
        logger.info("Serving model in GC AI platform...")
        serve_model_use_case.execute()
        message = "Model version is being created in GCP AI Platform."
        logger.info(message)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": message}
        )
    except Exception as err:
        message = f"Error serving the model: {str(err)}"
        logger.error(message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": message},
        )


# uvicorn src.serve_model.infrastructure.serve_model_api_controller:rest_api --port 1219
