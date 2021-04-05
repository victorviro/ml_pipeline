import logging
import os

from mlflow import start_run, log_artifact, get_artifact_uri, log_dict
from sklearn.pipeline import Pipeline

from src.shared.interfaces.data_tracker import IDataTracker


logger = logging.getLogger(__name__)


class MlflowTracker(IDataTracker):
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
        :type model_name: Pipeline
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
                artifact_path = f'{os.getcwd()}/{model_artifact_uri}/{filename}'
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
