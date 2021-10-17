import logging
from typing import Any, Dict

from mlflow import (
    get_artifact_uri,
    get_run,
    log_dict,
    log_metrics,
    log_params,
    set_tags,
    start_run,
)
from mlflow.sklearn import load_model
from mlflow.sklearn import log_model as log_sklearn_model

from src.shared.constants import MODEL_NAME, TRANSFORMER_PIPELINE_NAME
from src.shared.interfaces.data_tracker import IDataTracker

logger = logging.getLogger(__name__)


class MlflowPythonTracker(IDataTracker):
    def __init__(self, run_id: str):
        """
        :param run_id: The MLflow run id of the experiment run
        :type run_id: str
        """
        self.run_id = run_id

    def log_information_of_data_versioning(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        self._track_tags(tags=information_to_log)

    def log_information_of_data_preprocessor_fitting(
        self, data_preprocessor: Any
    ) -> None:
        self._track_sklearn_model(
            model=data_preprocessor, model_name=TRANSFORMER_PIPELINE_NAME
        )
        # Get dict with information of the preprocessing steps
        preprocessing_steps = {"preprocessing_steps": [*data_preprocessor.named_steps]}
        self._track_dict(
            dictionary=preprocessing_steps,
            run_relative_file_path=f"{TRANSFORMER_PIPELINE_NAME}.json",
        )

    def log_information_of_model_training(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        # Track parameters
        self._track_parameters(parameters=information_to_log["parameters"])
        # Track the pipeline in the experiment run
        self._track_sklearn_model(
            model=information_to_log["pipeline"], model_name=MODEL_NAME
        )

    def log_information_of_model_evaluation(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        self._track_metrics(metrics=information_to_log["metrics"])

    def load_model_logged(self, model_name: str) -> Any:
        # Get the artifacts uri of the experiment run
        artifacts_uri = self._get_artifacts_uri(model_name=model_name)
        model = self._load_sklearn_model(model_uri=artifacts_uri)
        return model

    def get_information_logged_for_model_validation(self) -> Dict[str, Any]:
        metrics: Dict[str, Any] = self._get_tracked_items(item_type="metric")
        return metrics

    def get_model_path_in_storage(self) -> str:
        # Get the artifacts uri of the experiment run
        artifacts_uri = self._get_artifacts_uri(model_name=MODEL_NAME)
        return f"{artifacts_uri}/"

    def _track_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Track metrics in a MLflow experiment run.
        """
        try:
            with start_run(run_id=self.run_id):
                log_metrics(metrics)
        except Exception as err:
            message = "Error tracking metrics in MLflow experiment."
            raise Exception(message) from err

    def _track_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Track parameters in a MLflow experiment run.

        :param parameters: The parameters to track
        :type parameters: dict
        """
        try:
            with start_run(run_id=self.run_id):
                log_params(parameters)
        except Exception as err:
            message = "Error tracking parameters in MLflow experiment."
            raise Exception(message) from err

    def _track_tags(self, tags: Dict[str, Any]) -> None:
        """
        Track tags in a MLflow experiment run.

        :param parameters: The tags to track
        :type parameters: dict
        """
        try:
            with start_run(run_id=self.run_id):
                set_tags(tags)
        except Exception as err:
            message = "Error tracking tags in MLflow experiment."
            raise Exception(message) from err

    def _track_sklearn_model(self, model: Any, model_name: str) -> None:
        """
        Track a sklearn model in a MLflow experiment run.

        :param model: The parameters to track
        :type model: Sklearn model
        :param model_name: The path inside the artifact uri where store the model
        :type model_name: str
        """
        try:
            with start_run(run_id=self.run_id):
                log_sklearn_model(sk_model=model, artifact_path=model_name)
        except Exception as err:
            message = "Error tracking sklearn model in MLflow experiment."
            raise Exception(message) from err

    def _track_dict(
        self, dictionary: Dict[Any, Any], run_relative_file_path: str
    ) -> None:
        """
        Track a dictionary into an MLflow experiment using the MLflow python API.

        :param dictionary: The dict to track
        :type dictionary: dict
        :param relative_file_path: The run-relative artifact file path to which the dict
            is saved
        :type relative_file_path: str
        """
        try:
            with start_run(run_id=self.run_id):
                log_dict(dictionary=dictionary, artifact_file=run_relative_file_path)
        except Exception as err:
            message = "Error tracking dictionary in MLflow experiment."
            raise Exception(message) from err

    def _get_artifacts_uri(self, model_name: str) -> str:
        """
        Get the artifacts path of the MLflow experiment run.

        :param model_name: The path inside the artifact uri where the artifacts are stored
        :type model_name: str
        :return: The artifacts path
        :rtype: str
        """
        try:
            with start_run(run_id=self.run_id):
                # Get the model artifact uri
                model_artifact_uri: str = get_artifact_uri(model_name)
                logger.info(f"Artifacts uri gotten: {model_artifact_uri}")
                return model_artifact_uri
        except Exception as err:
            message = "Error getting artifacts uri from a MLflow run."
            raise Exception(message) from err

    def _load_sklearn_model(self, model_uri: str) -> Any:
        """
        Load a sklearn model from a MLflow run.

        :param model_uri: The location, in URI format, of the MLflow model
        :type model_uri: str
        :return: The sklearn model
        :rtype:
        """
        try:
            with start_run(run_id=self.run_id):
                model = load_model(model_uri=model_uri)
                logger.info(
                    "Sklearn model loaded succesfully from a MLflow run. Model "
                    f"uri: {model_uri}"
                )
                return model
        except Exception as err:
            message = (
                "Error loading sklearn model from a MLflow run. Model uri: "
                f"{model_uri}."
            )
            raise Exception(message) from err

    def _get_tracked_items(self, item_type: str) -> Dict[str, Any]:
        """
        Get items (parameters, metrics or tags) tracked in the MLflow experiment run.

        :param item_type: The type of the item (metric, parameter or tag)
        :type item_type: str
        :return: The items tracked in the experiment run
        :rtype: dict
        """
        try:
            run_info = get_run(run_id=self.run_id)
            items_info: Dict[str, Any] = {}
            if item_type == "metric":
                items_info = run_info.data.metrics
            if item_type == "parameter":
                items_info = run_info.data.params
            if item_type == "tag":
                items_info = run_info.data.tags
            if not items_info:
                logger.warning(
                    f"The are no {item_type}s tracked in the experiment run "
                    f'with id: "{self.run_id}"'
                )
            return items_info
        except Exception as err:
            message = (
                f"Error getting {item_type}s from the mlflow experiment run with "
                f'id: "{self.run_id}".'
            )
            logger.error(message)
            raise Exception(message) from err
