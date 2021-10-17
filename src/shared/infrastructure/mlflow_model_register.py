import logging

from mlflow import register_model as register_model_in_mlflow_registry
from mlflow import start_run
from mlflow.tracking import MlflowClient

from src.shared.constants import MODEL_NAME
from src.shared.interfaces.model_register import IModelRegister, ModelStage

logger = logging.getLogger(__name__)


class MlflowModelRegister(IModelRegister):
    def __init__(self, run_id: str):
        """
        :param run_id: The MLflow run id of the experiment run
        :type run_id: str
        """
        self.run_id = run_id

    def register_model(self, name: str) -> None:
        """
        Register the model in MLflow registry (staged as None).

        :param name: Name of the registered model
        :type name: str
        """
        try:
            with start_run(run_id=self.run_id):
                # Build artifact uri where the model is stored
                model_uri = f"runs:/{self.run_id}/{MODEL_NAME}"
                registered_model_info = register_model_in_mlflow_registry(
                    model_uri=model_uri, name=name
                )
                logger.info(
                    f"Model registered in MLflow Registry. Name: {name}. "
                    f"Version: {registered_model_info.version}"
                )
        except Exception as err:
            message = "Error registering model in MLflow Registry."
            raise Exception(message) from err

    @staticmethod
    def get_stage_from_enum(stage: ModelStage) -> str:
        mlflow_stages = {
            ModelStage.UNDEFINED: "None",
            ModelStage.STAGING: "Staging",
            ModelStage.PRODUCTION: "Production",
            ModelStage.ARCHIVED: "Archived",
        }
        return mlflow_stages[stage]

    def transition_model_version_stage(self, name: str, stage: str) -> None:
        """
        Update model version stage in MLflow Registry.

        :param name: Name of the registered model
        :type name: str
        :param stage: New desired stage for this model version
                      (None/Staging/Production/Archived)
        :type stage: str
        """
        # Get the version of the model registered
        version_model_registered = self._search_model_version_in_mlflow_registry()
        try:
            client = MlflowClient()
            # Update model version stage
            client.transition_model_version_stage(
                name=name, stage=stage, version=version_model_registered
            )
            logger.info(
                "Updated stage of model registered in MLflow Registry to "
                f'"{stage}"". Name: {name}. '
                f"Version: {version_model_registered}."
            )
        except Exception as err:
            message = (
                f'Error updating stage of model "{name}" with '
                f'version "{version_model_registered}" in MLflow Registry. '
            )
            logger.error(message)
            raise Exception(message) from err

    def _search_model_version_in_mlflow_registry(self) -> str:
        """
        Get the model version of a run registered in MLFLOW Registry.

        :return: The model version
        :rtype: str
        """
        try:
            client = MlflowClient()
            # Get the version of the model filtered by run id
            filter_string = f"run_id='{self.run_id}'"
            results = client.search_model_versions(filter_string=filter_string)
            version_model_registered: str = results[0].version
            return version_model_registered
        except Exception as err:
            message = "Error getting model version of a run in MLflow Registry."
            logger.error(message)
            raise Exception(message) from err
