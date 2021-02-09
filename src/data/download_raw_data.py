

import logging
import requests
from requests.exceptions import ConnectionError
import click

from src.config_variables import (ENDPOINT_URL, RAW_DATA_PATH, MCPL_ENDPOINT_NAME)
from src.utils.files import save_json_file


logger = logging.getLogger(__name__)


@click.option("--data_name", type=click.Choice(['MCPL']),
              help="The dataset to download")
def download_raw_data(data_name: str):
    """
    Get raw data for max char per line prediction. It sends a request to the
    quotes_image REST API to bring the data. Then, it's stored in '../data/01_raw.
    It's assumed that the REST API is running.

    :param data_name: Name of the dataset to be stored
    :type data_name: str
    :raises Exception: Connection error
    """

    logger.info('======'*7)
    logger.info(f'Getting raw data. Name: {data_name}')

    # Get endpoint request path to fetch the dataset
    endpoint_path = f'{ENDPOINT_URL}{MCPL_ENDPOINT_NAME}/'

    try:
        # Request to get dataset
        request = requests.get(endpoint_path)
        logger.info(f'Request done. Storing dataset in {RAW_DATA_PATH}')
    except ConnectionError:
        msg = ('\nConnection error. Check that the quotes image backend is running or'
               ' that the name of the endpoint is correct.')
        raise Exception(msg)

    # Get the response json of the request
    raw_data = request.json()

    # Store the dataset
    full_data_path = f'{RAW_DATA_PATH}/{data_name}.json'
    save_json_file(file_path=full_data_path, content=raw_data)
    logger.info(f'Stored dataset in {full_data_path}')
    logger.info('======'*7)


if __name__ == '__main__':
    download_raw_data()
