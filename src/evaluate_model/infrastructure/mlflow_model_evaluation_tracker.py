
from src.shared.infrastructure.mlflow_api_tracker import MlflowApiTracker


class MlflowModelEvaluationTracker(MlflowApiTracker):
    """
    A class which extends the class MlflowApiTracker to track information of the
    model evaluation (metrics) to an MLflow experiment run using the
    MLflow REST API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """
    def __init__(self, run_id: str):
        super().__init__(run_id)

    def track_model_evaluation_info(self, information_to_track: dict):
        """
        Track information of the model evaluation (metrics) to an
        MLflow experiment run.

        :param information_to_track: The information to track
        :type information_to_track: dict
        """
        # Track metrics
        self.track_items(data=information_to_track["metrics"], item_type='metrics')
