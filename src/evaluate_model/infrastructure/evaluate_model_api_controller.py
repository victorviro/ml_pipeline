import logging.config

from fastapi import status  # starlette statuses
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.evaluate_model.application.evaluate_model_use_case import EvaluateModel
from src.evaluate_model.infrastructure.sklearn_model_evaluator import (
    SklearnModelEvaluator,
)
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker
from src.shared.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    raw_data_path: str
    data_name: str
    size_test_split: float
    test_split_seed: int
    mlflow_run_id: str


rest_api = FastAPI()


@rest_api.post("/api/evaluate_model")
async def evaluate_model_endpoint(item: Item):
    model_evaluator = SklearnModelEvaluator(
        size_test_split=item.size_test_split, test_split_seed=item.test_split_seed
    )
    data_loader = JSONDataLoader()
    data_tracker = MlflowPythonTracker(run_id=item.mlflow_run_id)

    evaluate_model_use_case = EvaluateModel.build(
        model_evaluator=model_evaluator,
        dataset_file_loader=data_loader,
        data_tracker=data_tracker,
    )
    dataset_file_path = f"{item.raw_data_path}/{item.data_name}.json"

    try:
        logger.info("Evaluating the model...")
        evaluate_model_use_case.execute(dataset_file_path=dataset_file_path)
        message = "Model evaluated succesfully and metrics tracked."
        logger.info(message)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": message}
        )
    except Exception as err:
        message = f"Error evaluating the model. Error description: {str(err)}."
        logger.error(message)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": message},
        )


# uvicorn src.evaluate_model.infrastructure.evaluate_model_api_controller:rest_api --port
# 1220
