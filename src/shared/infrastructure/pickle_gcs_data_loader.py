import pickle
import logging

from google.cloud import storage

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.constants import GCP_PROJECT_NAME, GCP_BUCKET_NAME


logger = logging.getLogger(__name__)


class PickleGCSDataLoader(IDataFileLoader):
    """
    A class which implements the interface IDataFileLoader to load data from files.
    It loads pickle data from Google CLoud Storage.
    """

    def load_data(self, file_path: str):
        """
        Load pickle data from a file from Google CLoud Storage.
        """
        storage_client = storage.Client()
        gcs_client = storage.Client(project=GCP_PROJECT_NAME)
        bucket = gcs_client.get_bucket(GCP_BUCKET_NAME)

        blob = bucket.blob(file_path)
        file_encoded = blob.download_as_bytes()
        file = pickle.loads(file_encoded, encoding='bytes')

        msg = f'Pickle data file loaded succesfully from GCS. Path: {file_path}'
        logger.info(msg)
        return file
