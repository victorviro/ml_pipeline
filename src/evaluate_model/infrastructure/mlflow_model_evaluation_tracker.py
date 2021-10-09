from sklearn.pipeline import Pipeline

from src.shared.constants import MODEL_NAME
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowModelEvaluationTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    model evaluation (metrics) to an MLflow experiment run using the MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def track_model_evaluation_info(self, information_to_track: dict):
        """
        Track information of the model evaluation (metrics) to an
        MLflow experiment run.

        :param information_to_track: The information to track
        :type information_to_track: dict
        """
        self.track_metrics(metrics=information_to_track["metrics"])

    def get_tracked_model(self) -> Pipeline:
        """
        Get the sklearn model tracked in the MLflow experiment run.

        :return: The sklearn model
        :rtype: Pipeline
        """
        # Get the artifacts uri of the experiment run
        artifacts_uri = self.get_artifacts_uri(model_name=MODEL_NAME)
        model = self.load_sklearn_model(model_uri=artifacts_uri)
        return model
