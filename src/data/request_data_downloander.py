import logging
import requests
from requests.exceptions import ConnectionError


from src.config_variables import (RAW_DATA_PATH, ENDPOINT_PATH)
from src.utils.files import save_json_file


logger = logging.getLogger(__name__)


class RequestDataDownloander():
    def __init__(self, endpoint_path: str, data_path: str, data_name: str):

        self.data_path = data_path
        self.data_name = data_name
        self.endpoint_path = endpoint_path

    def download_data(self):

        logger.info('======'*7)
        logger.info(f'Getting raw data. Name: {self.data_name}')
        try:
            # Request to get dataset
            request = requests.get(self.endpoint_path)
            logger.info(f'Request done. Storing dataset in {self.data_path }')
        except ConnectionError:
            msg = ('\nConnection error. Check that the quotes image backend is running or'
                   ' that the name of the endpoint is correct.')
            raise Exception(msg)

        # Get the response json of the request
        raw_data = request.json()
        # Store the dataset
        full_data_path = f'{self.data_path }/{self.data_name}.json'
        self.save_data(data=raw_data, full_data_path=full_data_path)

    def save_data(self, data: dict, full_data_path: str):
        save_json_file(file_path=full_data_path, content=data)
        logger.info(f'Stored dataset in {full_data_path}')
        logger.info('======'*7)
