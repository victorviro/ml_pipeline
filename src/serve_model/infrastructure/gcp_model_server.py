import logging
from os import getenv

from google.api_core.client_options import ClientOptions
from googleapiclient import discovery, errors

from src.serve_model.domain.model_server import IModelServer
from src.shared.constants import GCP_MODEL_NAME, GCP_REGION

logger = logging.getLogger(__name__)


GCP_ENDPOINT = f"https://{GCP_REGION}-ml.googleapis.com"
GCP_PARENT = f'projects/{getenv("GCP_PROJECT_ID")}/models/{GCP_MODEL_NAME}'
GCP_MODEL_VERSION_BODY = {
    "name": "",
    "deploymentUri": "",
    "runtimeVersion": "2.4",
    "framework": "scikit-learn",
    "pythonVersion": "3.7",
    "machineType": getenv("GCP_PREDICTION_MACHINE_TYPE"),
}


class GCPModelServer(IModelServer):
    @staticmethod
    def create_model_version(version_name: str, model_gcs_path: str):
        """
        Create a new version of a model in GCP AI Platform.

        :param version_name: The name of the model's version to set in GCP AI Platform
        :type version_name: str
        :param model_gcs_path: The path of the scikit-learn model in GCS
        :type model_gcs_path: str
        """
        # Create the AI Platform service object
        client_options = ClientOptions(api_endpoint=GCP_ENDPOINT)
        service = discovery.build("ml", "v1", client_options=client_options)
        # Create a request to call projects.models.versions.create.
        GCP_MODEL_VERSION_BODY.update(
            {"name": version_name, "deploymentUri": model_gcs_path}
        )

        request = (
            service.projects()  # pylint: disable=maybe-no-member
            .models()
            .versions()
            .create(parent=GCP_PARENT, body=GCP_MODEL_VERSION_BODY)
        )
        try:
            response = request.execute()
            logger.info(
                "Model version is being created in GCP AI Platform. "
                f"Model name: {GCP_MODEL_NAME}. Version name: {version_name}. "
                f"Response:\n{response}"
            )
        except errors.HttpError as err:
            msg = "There was an error creating the model version."
            logger.error(msg)
            raise Exception(msg) from err

    def serve_model(self, model_path: str, model_version: float):
        """
        Serve a model version in GCP AI Platform (it is assumed a model is already
        created in GCP AI Platform).

        :param model_path: The path of the scikit-learn model in GCS
        :type model_path: str
        :param model_version: The model's version to set in GCP AI Platform
        :type model_version: str
        """

        # Create a model version in GCP AI Platform
        self.create_model_version(
            version_name=f"v_{model_version}", model_gcs_path=model_path
        )
