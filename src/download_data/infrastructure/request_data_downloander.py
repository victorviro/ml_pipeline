import logging
import requests

from src.shared.files_helper import save_json_file


logger = logging.getLogger(__name__)


class RequestDataDownloander():
    def __init__(self, url_quotes_image_api_mcpl_data: str, data_path: str,
                 data_name: str):

        self.data_path = data_path
        self.data_name = data_name
        self.url_quotes_image_api_mcpl_data = url_quotes_image_api_mcpl_data
        self.full_data_path = f'{data_path}/{data_name}.json'

    def download_data(self):

        logger.info(f'Getting raw data. Name: {self.data_name}')
        # Launch the request to get the data
        try:
            request_response = requests.get(self.url_quotes_image_api_mcpl_data)
            msg = f'Request done succesfully.'
            logger.info(msg)
        except Exception as err:

            if isinstance(err, requests.exceptions.ConnectionError):
                msg = ('Connection error. Check that the quotes image backend is'
                       ' running or that the path of the endpoint is correct.')
                logger.error(msg)
                raise Exception(msg)
            msg = f'Error when request data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Get the response json of the request
        try:
            raw_data = request_response.json()
            msg = ('Gotten the json response from the request response. Storing '
                   f'dataset in {self.data_path}')
            logger.info(msg)

        except Exception as err:
            msg = f'Error getting the json from the request response. Taceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        # Store the dataset
        try:
            save_json_file(file_path=self.full_data_path, content=raw_data)
            msg = f'Dataset stored succesfully in path: {self.full_data_path}'
            logger.info(msg)
        except Exception as err:
            msg = f'Error storing the dataset. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
