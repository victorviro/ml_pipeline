import logging

from mlflow import (
    get_artifact_uri,
    get_run,
    log_dict,
    log_metrics,
    log_params,
    register_model,
    set_tags,
    start_run,
)
from mlflow.sklearn import load_model
from mlflow.sklearn import log_model as log_sklearn_model
from mlflow.tracking import MlflowClient

from src.shared.constants import REGISTRY_MODEL_NAME
from src.shared.interfaces.data_tracker import IDataTracker

logger = logging.getLogger(__name__)


class MlflowPythonTracker(IDataTracker):
    """
    A class which implements the interface IDataTracker to track data to an experiment.
    It tracks data (metrics, models,...) into an MLflow experiment using the
    MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def __init__(self, run_id: str):
        self.run_id = run_id

    @staticmethod
    def track_data():
        return NotImplementedError

    def track_metrics(self, metrics: dict):
        """
        Track metrics in a MLflow experiment run.

        :param metrics: The metrics to track
        :type metrics: dict
        """
        try:
            with start_run(run_id=self.run_id):
                log_metrics(metrics)
        except Exception as err:
            message = "Error tracking metrics in MLflow experiment."
            raise Exception(message) from err

    def track_parameters(self, parameters: dict):
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

    def track_tags(self, tags: dict):
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

    def track_sklearn_model(self, model, model_name: str):
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

    def track_dict(self, dictionary: dict, run_relative_file_path: str):
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

    def register_model(self, model_name: str, name: str):
        """
        Register the model in MLflow registry (staged as None)

        :param model_name: The path inside the artifact uri where the model is stored
        :type model_name: str
        :param name: Name of the registered model
        :type name: str
        """
        try:
            with start_run(run_id=self.run_id):
                model_uri = f"runs:/{self.run_id}/{model_name}"
                registered_model_info = register_model(model_uri=model_uri, name=name)
                logger.info(
                    f"Model registered in MLflow Registry. Name: {name}. "
                    f"Version: {registered_model_info.version}"
                )
        except Exception as err:
            message = "Error registering model in MLflow Registry."
            raise Exception(message) from err

    def get_artifacts_uri(self, model_name: str) -> str:
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
                model_artifact_uri = get_artifact_uri(model_name)
                logger.info(f"Artifacts uri gotten: {model_artifact_uri}")
                return model_artifact_uri
        except Exception as err:
            message = "Error getting artifacts uri from a MLflow run."
            raise Exception(message) from err

    def load_sklearn_model(self, model_uri: str):
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

    def search_model_version(self) -> str:
        """
        Get the model version of a run registered in MLFLOW Registry.

        :return: The model version
        :rtype: str
        """
        try:
            client = MlflowClient()
            # Get the version of the model filtered by run id
            filter_string = f"run_id='{self.run_id}'"
            results = client.search_model_versions(filter_string=filter_string)
            version_model_registered = results[0].version
            return version_model_registered
        except Exception as err:
            message = "Error getting model version of a run in MLflow Registry."
            logger.error(message)
            raise Exception(message) from err

    def transition_model_version_stage(self, stage: str):
        """
        Update model version stage in MLflow Registry.

        :param stage: New desired stage for this model version (None/staging/production)
        :type stage: str
        """
        # Get the version of the model registered
        version_model_registered = self.search_model_version()
        try:
            client = MlflowClient()
            # Update model version stage
            client.transition_model_version_stage(
                name=REGISTRY_MODEL_NAME, stage=stage, version=version_model_registered
            )
            logger.info(
                "Updated stage of model registered in MLflow Registry to "
                f'"{stage}"". Name: {REGISTRY_MODEL_NAME}. '
                f"Version: {version_model_registered}."
            )
        except Exception as err:
            message = (
                f'Error updating stage of model "{REGISTRY_MODEL_NAME}" with '
                f'version "{version_model_registered}" in MLflow Registry. '
            )
            logger.error(message)
            raise Exception(message) from err

    def get_tracked_items(self, item_type: str) -> dict:
        """
        Get items (parameters, metrics or tags) tracked in the MLflow experiment run.

        :param item_type: The type of the item (metric, parameter or tag)
        :type item_type: str
        :return: The items tracked in the experiment run
        :rtype: dict
        """
        try:
            run_info = get_run(run_id=self.run_id)
            if item_type == "metric":
                items_info = run_info.data.metrics
            if item_type == "parameter":
                items_info = run_info.data.params
            if item_type == "tag":
                items_info = run_info.data.metrics
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
