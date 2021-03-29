import logging
import requests

from src.get_data.domain.data_downloander import IDataDownloander

logger = logging.getLogger(__name__)


class RequestDataDownloander(IDataDownloander):
    """
    A class which implements the interface IDataDownloander to download data.
    It gets the data through a request.
    """

    def download_data(self, data_api_url: str) -> dict:
        """
        Download the data through a request.

        :param data_api_url: Url of the API to get the data
        :type data_api_url: str
        :return: The data downloaded
        :rtype: dict
        """

        logger.info(f'Getting raw data through a request.')
        # Launch the request to get the data
        try:
            request_response = requests.get(data_api_url)
            msg = f'Request done succesfully.'
            logger.info(msg)
        except Exception as err:

            if isinstance(err, requests.exceptions.ConnectionError):
                msg = ('Connection error. Check that the quotes image API is'
                       ' running or that the path of the endpoint is correct.')
                logger.error(msg)
                raise Exception(msg)
            msg = f'Error when request data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Get the response json of the request
        try:
            raw_data = request_response.json()
            msg = ('Gotten the data succesfully from the request response.')
            logger.info(msg)

        except Exception as err:
            msg = f'Error getting the json from the request response. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        return raw_data
