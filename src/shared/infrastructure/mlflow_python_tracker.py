import logging

from mlflow import (start_run, get_artifact_uri, log_dict, log_params,
                    log_metrics, register_model)
from mlflow.sklearn import log_model as log_sklearn_model
from mlflow.sklearn import load_model

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

    def track_data(self):
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
            message = f'Error tracking metrics in MLflow experiment: {str(err)}'
            raise Exception(message)

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
            message = f'Error tracking parameters in MLflow experiment: {str(err)}'
            raise Exception(message)

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
            message = f'Error tracking sklearn model in MLflow experiment: {str(err)}'
            raise Exception(message)

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
            message = f'Error tracking dictionary in MLflow experiment: {str(err)}'
            raise Exception(message)

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
                model_uri = f'runs:/{self.run_id}/{model_name}'
                registered_model_info = register_model(model_uri=model_uri,
                                                       name=name)
                logger.info(f'Model registered in MLflow Registry. Name: {name}. '
                            f'Version: {registered_model_info.version}')
        except Exception as err:
            message = f'Error registering model in MLflow Registry: {str(err)}'
            raise Exception(message)

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
                logger.info(f'Artifacts uri gotten: {model_artifact_uri}')
                return model_artifact_uri
        except Exception as err:
            message = f'Error getting artifacts uri from a MLflow run: {str(err)}'
            raise Exception(message)

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
                logger.info('Sklearn model loaded succesfully from a MLflow run. Model '
                            f'uri: {model_uri}')
                return model
        except Exception as err:
            message = ('Error loading sklearn model from a MLflow run. Model uri: '
                       f'{model_uri}. Error description: {str(err)}')
            raise Exception(message)
