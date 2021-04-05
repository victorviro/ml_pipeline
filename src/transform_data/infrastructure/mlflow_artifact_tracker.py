import logging
import os

import mlflow
from sklearn.pipeline import Pipeline

from src.shared.interfaces.data_tracker import IDataTracker


logger = logging.getLogger(__name__)


class MlflowArtifactTracker(IDataTracker):
    """
    A class which implements the interface IDataTracker to track data to an experiment.
    It tracks data of an artifact into an MLflow experiment using the MLflow python API.

    :param run_id: The MLflow run id
    :type run_id: str
    :param model_name: The dir within the experiment uri to store the file
    :type model_name: str
    """
    def __init__(self, run_id: str, model_name: str):
        self.run_id = run_id
        self.model_name = model_name

    def track_data(self, artifact_path: str, transformer: Pipeline):
        """
        Track data of an artifact into an MLflow experiment using the MLflow python API.

        :param artifact_path: The local path of the artifact to track
        :type artifact_path: str
        :param transformer: The transformer sklearn pipeline
        :type transformer: Pipeline
        """
        try:
            with mlflow.start_run(run_id=self.run_id):
                # Track transformer pipeline file in MLflow
                mlflow.log_artifact(
                    local_path=artifact_path,
                    artifact_path=self.model_name
                )
                logger.info('Transformer pipeline tracked in MLflow experiment')
                # Track in MLflow name of steps of the transformer pipe in a dict
                transformer_steps = {'transformer_steps': [*transformer.named_steps]}
                mlflow.log_dict(transformer_steps, 'transformer_pipe.json')
                # Get the path of the artifact
                pipe_filename = os.path.basename(artifact_path)
                model_artifact_uri = mlflow.get_artifact_uri(self.model_name)
                artifact_path = f'{os.getcwd()}/{model_artifact_uri}/{pipe_filename}'
                return artifact_path
        except Exception as err:
            message = f'Error tracking transformer pipe in MLflow experiment: {str(err)}'
            raise Exception(message)
