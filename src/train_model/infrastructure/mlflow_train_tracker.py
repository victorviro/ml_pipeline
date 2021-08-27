from sklearn.pipeline import Pipeline

from src.shared.constants import (
    MODEL_NAME,
    REGISTRY_MODEL_NAME,
    TRANSFORMER_PIPELINE_NAME,
)
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowTrainTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    model training (parameters, models,...) to an MLflow experiment run using the
    MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """
    def __init__(self, run_id: str):
        super().__init__(run_id)

    def track_training_info(self, information_to_track: dict):
        """
        Track information of the model training (metrics, models,...) to a
        MLflow experiment run.

        :param information_to_track: The information to track
        :type information_to_track: dict
        """
        # Track parameters
        self.track_parameters(parameters=information_to_track["parameters"])

        # Track the pipeline in the experiment run
        self.track_sklearn_model(model=information_to_track["pipeline"],
                                 model_name=MODEL_NAME)
        # Register the model in model registry (staged as None)
        self.register_model(model_name=MODEL_NAME, name=REGISTRY_MODEL_NAME)

    def get_tracked_transformer(self) -> Pipeline:
        """
        Get the transformer sklearn pipeline tracked in the MLflow experiment run.

        :return: The transformer sklearn pipeline
        :rtype: Pipeline
        """
        # Get the artifacts uri of the experiment run
        artifacts_uri = self.get_artifacts_uri(model_name=TRANSFORMER_PIPELINE_NAME)
        model = self.load_sklearn_model(model_uri=artifacts_uri)
        return model
