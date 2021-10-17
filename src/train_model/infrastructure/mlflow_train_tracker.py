from sklearn.pipeline import Pipeline

from src.shared.constants import MODEL_NAME, TRANSFORMER_PIPELINE_NAME
from src.shared.infrastructure.mlflow_python_tracker import MlflowPythonTracker


class MlflowTrainTracker(MlflowPythonTracker):
    def track_training_metadata(self, metadata_to_track: dict):
        """
        Track metadata of the model training (metrics, models,...) to a
        MLflow experiment run.

        :param metadata_to_track: Metadata about training to track
        :type metadata_to_track: dict
        """
        # Track parameters
        self.track_parameters(parameters=metadata_to_track["parameters"])

        # Track the pipeline in the experiment run
        self.track_sklearn_model(
            model=metadata_to_track["pipeline"], model_name=MODEL_NAME
        )

    def get_tracked_preprocesser(self) -> Pipeline:
        """
        Get the preprocesser sklearn pipeline tracked in the MLflow experiment run.

        :return: The preprocesser sklearn pipeline
        :rtype: Pipeline
        """
        # Get the artifacts uri of the experiment run
        artifacts_uri = self.get_artifacts_uri(model_name=TRANSFORMER_PIPELINE_NAME)
        preprocesser = self.load_sklearn_model(model_uri=artifacts_uri)
        return preprocesser
