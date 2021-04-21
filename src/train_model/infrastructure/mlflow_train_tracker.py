
from src.shared.constants import MODEL_NAME, REGISTRY_MODEL_NAME
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowTrainTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    model training (metrics, models,...) to an MLflow experiment run using the
    MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """
    def __init__(self, run_id: str):
        super().__init__(run_id)

    def track_training_info(self, information_to_track: dict):
        """
        Track information of the model training (metrics, models,...) to an
        MLflow experiment run.

        :param information_to_track: The information to track
        :type information_to_track: dict
        """

        self.track_metrics(metrics=information_to_track["metrics"])

        self.track_parameters(parameters=information_to_track["parameters"])
        # Track the model in the experiment run
        self.track_sklearn_model(model=information_to_track["model"],
                                 model_name=MODEL_NAME)
        # Register the model in model registry (staged as None)
        self.register_model(model_name=MODEL_NAME, name=REGISTRY_MODEL_NAME)
