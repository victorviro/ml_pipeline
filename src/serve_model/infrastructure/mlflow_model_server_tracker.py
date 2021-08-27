
from src.shared.constants import MODEL_NAME
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowModelServerTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to get tracked information
    in a MLflow experiment run using the MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """

    def __init__(self, run_id: str):
        super().__init__(run_id)

    def get_tracked_model_path(self) -> str:
        """
        Get the path of the sklearn model tracked in the MLflow experiment run.

        :return: The path of the sklearn model tracked
        :rtype: str
        """
        # Get the artifacts uri of the experiment run
        artifacts_uri = self.get_artifacts_uri(model_name=MODEL_NAME)
        return f'{artifacts_uri}/'

    def get_model_version_in_registry(self) -> str:
        """
        Get the version of the model tracked in MLflow Registry.

        :return: The version of the model
        :rtype: str
        """
        model_version = self.search_model_version()
        return model_version
