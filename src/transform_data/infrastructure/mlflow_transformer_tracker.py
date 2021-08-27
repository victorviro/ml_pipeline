from sklearn.pipeline import Pipeline

from src.shared.constants import TRANSFORMER_PIPELINE_NAME
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

    def track_transformer_fitting_info(self, transformer: Pipeline):
        """
        Track information of the transformer fitting (transformer pipeline, preprocessing
        steps,...) to an MLflow experiment run.

        :param transformer: The sklearn transformer pipeline fitted
        :type transformer: Pipeline
        """
        # Track the transformer pipeline
        self.track_sklearn_model(
            model=transformer, model_name=TRANSFORMER_PIPELINE_NAME
        )
        # Get dict with information of the preprocessing steps
        transformer_steps = {"transformer_steps": [*transformer.named_steps]}
        self.track_dict(
            dictionary=transformer_steps,
            run_relative_file_path=f"{TRANSFORMER_PIPELINE_NAME}.json",
        )
