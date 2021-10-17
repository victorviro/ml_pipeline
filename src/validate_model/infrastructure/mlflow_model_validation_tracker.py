from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowModelValidationTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    model evaluation to an MLflow experiment run using the MLflow python API. It also
    updates the stage of the model in model Registry.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def get_metrics(self) -> dict:
        """
        Get metrics tracked in the MLflow experiment run.

        :return: The metrics
        :rtype: dict
        """
        metrics = self.get_tracked_items(item_type="metric")
        return metrics
