from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowDataVersioningTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    data versioning to an MLflow experiment run using the MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def __init__(self, run_id: str):
        super().__init__(run_id)

    def track_information(self, information_to_track: dict):
        """
        Track information of the data versioning (dataset path in the remote storage,
        version of the dataset...) to an MLflow experiment run.

        :param information_to_track: The information to track
        :type information_to_track: dict
        """
        self.track_tags(tags=information_to_track)
