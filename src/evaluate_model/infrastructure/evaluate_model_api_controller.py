import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.shared.constants import MODEL_NAME, GCP_BUCKET_NAME
from src.shared.infrastructure.json_data_loader import JSONDataLoader
from src.evaluate_model.application.evaluate_model_use_case import EvaluateModel
from src.shared.infrastructure.pickle_gcs_data_loader import PickleGCSDataLoader
from .sklearn_model_evaluator import SklearnModelEvaluator
from .mlflow_model_evaluation_tracker import MlflowModelEvaluationTracker


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
        size_test_split=item.size_test_split,
        test_split_seed=item.test_split_seed
    )
    json_data_loader = JSONDataLoader()
    pickle_gcs_data_loader = PickleGCSDataLoader()
    mlflow_api_tracker = MlflowModelEvaluationTracker(run_id=item.mlflow_run_id)
    artifacts_path = mlflow_api_tracker.get_artifacts_path()

    evaluate_model_use_case = EvaluateModel.build(
        model_evaluator=sklearn_model_evaluator,
        dataset_file_loader=json_data_loader,
        model_file_loader=pickle_gcs_data_loader,
        data_tracker=mlflow_api_tracker
    )
    data_file_path = f'{item.raw_data_path}/{item.data_name}.json'
    model_gcs_url = f'{artifacts_path}/{MODEL_NAME}.pkl'
    model_gcs_path_in_bucket = model_gcs_url.replace(f'gs://{GCP_BUCKET_NAME}/', '')

    try:
        logger.info(f'Evaluating model...')
        evaluate_model_use_case.execute(
            data_file_path=data_file_path,
            model_path=model_gcs_path_in_bucket
        )
        message = 'Model evaluated succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error evaluating the model: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.evaluate_model.infrastructure.evaluate_model_api_controller:rest_api --port
# 1220
