import logging
import os

from mlflow import (start_run, log_artifact, get_artifact_uri, log_dict, log_params,
                    log_metrics, register_model)
from sklearn.pipeline import Pipeline
from mlflow.sklearn import log_model as log_sklearn_model

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

    def track_artifact(self, file_path: str, model_name: str) -> str:
        """
        Track a file as an artifact into an MLflow experiment using the MLflow python API.

        :param file_path: The local path of the file to track
        :type file_path: str
        :param model_name: The path inside the artifact uri where store the file
        :type model_name: str
        :return: The path of the artifact stored within the MLflow experiment
        :rtype: str
        """
        try:
            with start_run(run_id=self.run_id):
                # Track transformer pipeline file in MLflow
                log_artifact(
                    local_path=file_path,
                    artifact_path=model_name
                )
                logger.info(f'File in path "{file_path}" tracked in MLflow experiment '
                            f'with id: "{self.run_id}".')
                # Get the path of the artifact
                filename = os.path.basename(file_path)
                model_artifact_uri = get_artifact_uri(model_name)
                artifact_path = f'{model_artifact_uri}/{filename}'
                return artifact_path
        except Exception as err:
            message = f'Error tracking file as artifact in MLflow experiment: {str(err)}'
            raise Exception(message)

    def track_sklearn_transfomer_pipeline(self, file_path: str, model_name: str,
                                          transformer_pipe: Pipeline) -> str:
        """Track a sklearn transformer pipeline as an artifact into an MLflow experiment
        using the MLflow python API.

        :param file_path: The local path of the sklearn transformer pipeline to track
        :type file_path: str
        :param model_name: The path inside the artifact uri where store the file
        :type model_name: str
        :param transformer_pipe: The sklearn transformer pipeline
        :type transformer_pipe: Pipeline
        :return: The path of the artifact stored within the MLflow experiment
        :rtype: str
        """
        try:
            # Track the file as an artifact into an MLflow experiment
            artifact_path = self.track_artifact(file_path=file_path,
                                                model_name=model_name)
            # Track in MLflow the name of steps of the transformer pipe in a dict
            with start_run(run_id=self.run_id):
                transformer_steps = {'transformer_steps': [*transformer_pipe.named_steps]}
                log_dict(transformer_steps, 'transformer_pipe.json')
            return artifact_path
        except Exception as err:
            message = f'Error tracking transformer pipe in MLflow experiment: {str(err)}'
            raise Exception(message)

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
                logger.info('Model registered in MLflow Registry. '
                            f'Name: {name}. '
                            f'Version: {registered_model_info.version}')
        except Exception as err:
            message = f'Error registering model in MLflow Registry: {str(err)}'
            raise Exception(message)

    def get_artifacts_path(self, model_name: str) -> str:
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
                # Get the artifacts path
                artifacts_path = f'{os.getcwd()}/{model_artifact_uri}'
                logger.info(f'Artifacts path gotten: {artifacts_path}')
                return artifacts_path
        except Exception as err:
            message = f'Error getting artifacts path from a MLflow run: {str(err)}'
            raise Exception(message)
