import logging
from json.decoder import JSONDecodeError

import requests
from requests.exceptions import ConnectionError

from src.get_data.domain.data_downloander import IDataDownloander

logger = logging.getLogger(__name__)


class RequestDataDownloander(IDataDownloander):
    """
    A class which implements the interface IDataDownloander to download data.
    It gets the data through a request.

    :param data_api_url: Url of the API to get the data
    :type data_api_url: str
    """

    def __init__(self, data_api_url: str):
        self.data_api_url = data_api_url

    def download_data(self) -> dict:
        """
        Download the data through a request.

        :return: The data downloaded
        :rtype: dict
        """

        logger.info(f"Getting raw data through a request.")
        # Launch the request to get the data
        try:
            # ping
            request_response = requests.get(self.data_api_url)
            if request_response.status_code == 200:
                logger.info("Request to get the dataset done succesfully.")
            else:
                msg = (
                    "Request to get the dataset was wrong. Status code of request: "
                    f"{request_response.status_code}"
                )
                logger.error(msg)
                raise Exception(msg)

        except ConnectionError as err:
            msg = (
                "Connection error when request dataset. Check that the API is running "
                f"or the endpoint is correct. Traceback of error: {err}"
            )
            logger.error(msg)
            raise ConnectionError(msg)

        except Exception as err:
            msg = (
                f"Unknown error when request data. Traceback: {err.__class__.__name__}"
                f": {err}"
            )
            logger.error(msg)
            raise Exception(msg)

        # Get the response json of the request
        try:
            raw_data = request_response.json()
            logger.info("Gotten the dataset succesfully from the request response.")

        except JSONDecodeError as err:
            msg = (
                "JSON decode error when getting the json from the request response. "
                f"The request response contains invalid JSON. Traceback: {err}"
            )
            logger.error(msg)
            raise JSONDecodeError(msg=msg, doc=err.doc, pos=err.pos)

        except Exception as err:
            msg = (
                "Unknown error getting the JSON from the request response. Traceback: "
                f"{err.__class__.__name__}: {err}"
            )
            logger.error(msg)
            raise Exception(msg)

        return raw_data
