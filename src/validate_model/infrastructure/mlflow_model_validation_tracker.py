
from src.shared.infrastructure.mlflow_api_tracker import MlflowApiTracker


class MlflowModelValidationTracker(MlflowApiTracker):
    """
    A class which extends the class MlflowApiTracker to track information of the
    model validation to an MLflow experiment run using the MLflow REST API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def __init__(self, run_id: str):
        super().__init__(run_id)

    def update_validated_model_in_registry(self):
        """
        Update the stage of the model to "Staging" in MLflow model registry.
        """
        self.transition_model_version_stage(stage='Staging')
