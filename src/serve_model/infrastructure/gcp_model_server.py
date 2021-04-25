import logging
from os import getenv

from google.cloud import storage
from googleapiclient import discovery, errors
from google.api_core.client_options import ClientOptions

from src.shared.constants import (GCP_BUCKET_NAME, GCP_MODEL_NAME, GCP_PROJECT_ID,
                                  GCP_REGION, GCP_PROJECT_NAME,
                                  GCP_MODEL_NAME_DESTINATION, GCP_PREDICTION_MACHINE_TYPE)
from src.serve_model.domain.model_server import IModelServer


logger = logging.getLogger(__name__)
GCP_ENDPOINT = f'https://{GCP_REGION}-ml.googleapis.com'
GCP_PARENT = f'projects/{GCP_PROJECT_ID}/models/{GCP_MODEL_NAME}'
GCP_MODEL_VERSION_BODY = {
  "name": '',
  "deploymentUri": f"gs://{GCP_BUCKET_NAME}/",
  "runtimeVersion": "2.4",
  "framework": "scikit-learn",
  "pythonVersion": "3.7",
  "machineType": GCP_PREDICTION_MACHINE_TYPE
}


class GCPModelServer(IModelServer):
    """
    A class which implements the interface IModelServer to serve the model in GCP AI
    Platform.
    """

    def upload_model_to_cloud_storage(self, model_file_path: str):
        """
        Copy/upload the model file to google cloud storage using the Cloud Storage
        Python API. This step wouln't be needed if we use GCP Cloud Storage as artifact
        store in MLFlow.

        :param model_file_path: The path of the scikit-learn pipeline
        :type model_file_path: str
        """
        try:
            gcs_client = storage.Client(project=GCP_PROJECT_NAME)
            bucket = gcs_client.get_bucket(GCP_BUCKET_NAME)
            blob = bucket.blob(GCP_MODEL_NAME_DESTINATION)
            blob.upload_from_filename(model_file_path)
            logger.info('Model uploaded to GCP cloud storage succesfully')
        except Exception as err:
            message = f'Error uploading the model file to GCP cloud storage: {str(err)}'
            logger.error(message)
            raise Exception(message)

    def create_model_version(self, version_name: str):
        """
        Create a model version in GCP AI Platform.

        :param version_name: The name of the model's version to set in GCP AI Platform
        :type version_name: str
        """
        # Create the AI Platform service object
        client_options = ClientOptions(api_endpoint=GCP_ENDPOINT)
        ml = discovery.build('ml', 'v1', client_options=client_options)
        # Create a request to call projects.models.versions.create.
        GCP_MODEL_VERSION_BODY.update({"name": version_name})
        request = ml.projects().models().versions().create(
            parent=GCP_PARENT,
            body=GCP_MODEL_VERSION_BODY
        )
        try:
            response = request.execute()
            logger.info('Model version created in GCP AI Platform succesfully.'
                        f' Version name: {version_name}. Response:\n{response}')
        except errors.HttpError as err:
            msg = ('There was an error creating the model version. Check the details:'
                   f' {err._get_reason()}')
            logger.error(msg)
            raise Exception(msg)

    def serve_model(self, model_file_path: str, version_name: str):
        """
        Serve a model version in GCP AI Platform.

        :param model_file_path: The path of the scikit-learn pipeline
        :type model_file_path: str
        :param version_name: The name of the model's version to set in GCP AI Platform
        :type version_name: str
        """
        # Upload the model file to google cloud storage
        self.upload_model_to_cloud_storage(model_file_path=model_file_path)
        # Create a model version in GCP AI Platform
        self.create_model_version(version_name=version_name)
