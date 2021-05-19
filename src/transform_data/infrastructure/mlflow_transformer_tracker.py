from sklearn.pipeline import Pipeline

from src.shared.constants import MODEL_NAME
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowTransformerTracker(MlflowPythonTracker):
    """
    A class which extends the class MlflowPythonTracker to track information of the
    transformer fitting (artifact, preprocessing steps,...) to an MLflow experiment run
    using the MLflow python API.

    :param run_id: The MLflow run id of the experiment run
    :type run_id: str
    """
    def __init__(self, run_id: str):
        super().__init__(run_id)

    def track_transformer_fitting_info(self, transformer: Pipeline,
                                       transformer_file_path: str):
        """
        Track information of the transformer fitting (artifact, preprocessing steps,...)
        to an MLflow experiment run.

        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        :param transformer_file_path: The path where the transformer file was stored
        :type transformer_file_path: str
        """
        self.track_sklearn_transfomer_pipeline(
            file_path=transformer_file_path,
            model_name=MODEL_NAME,
            transformer_pipe=transformer
        )
