import logging.config

from fastapi import status  # starlette statuses
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.evaluate_model.application.evaluate_model_use_case import EvaluateModel
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.shared.logging_config import LOGGING_CONFIG

from .mlflow_model_evaluation_tracker import MlflowModelEvaluationTracker
from .sklearn_model_evaluator import SklearnModelEvaluator

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
    sklearn_model_evaluator = SklearnModelEvaluator(
        size_test_split=item.size_test_split, test_split_seed=item.test_split_seed
    )
    json_data_loader = JSONDataLoader()
    mlflow_model_evaluation_tracker = MlflowModelEvaluationTracker(
        run_id=item.mlflow_run_id
    )

    evaluate_model_use_case = EvaluateModel.build(
        model_evaluator=sklearn_model_evaluator,
        dataset_file_loader=json_data_loader,
        data_tracker=mlflow_model_evaluation_tracker,
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
