from json import dumps
import requests
import logging

from src.shared.interfaces.data_tracker import IDataTracker


logger = logging.getLogger(__name__)


class MlflowApiTracker(IDataTracker):
    """
    A class which implements the interface IDataTracker to track data to an experiment.
    It tracks data into an MLflow experiment using requests to the MLflow Rest API.

    :param run_id: The MLflow run id
    :type run_id: str
    :param base_url: The base url of the MLflow Rest API
    :type base_url: str
    """
    def __init__(self, run_id: str, base_url: str):
        self.run_id = run_id
        self.base_url = base_url

    def track_data(self):
        return NotImplementedError

    def post(self, endpoint: str, body: dict):
        """
        Launch a POST request (to track information).

        :param endpoint: The endpoint of the MLflow Rest API to log batches of items
        :type endpoint: str
        :param body: The bofy of the POSt request
        :type body: dict
        """
        url = f'{self.base_url}/{endpoint}'
        # Track the information through a request
        try:
            request = requests.post(url, data=dumps(body))
            if request.status_code == 200:
                logger.info('Tracked experiment information in MLflow succesfully. '
                            f'Run id: {self.run_id}')
            else:
                msg = (f'Request post error: Status code: {request.status_code}. '
                       f'Content: {request.content}')
                raise Exception(msg)

        except Exception as err:
            message = ('Error tracking experiment information using the MLflow Rest Api.'
                       f'\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def track_items(self, data: dict, item_type: str, endpoint: str):
        """
        Track items (params, metrics or tags) into an MLflow experiment.

        :param data: The data information to track
        :type data: dict
        :param item_type: The type of items to track (tags/metrics/params)
        :type item_type: str
        :param endpoint: The endpoint of the MLflow Rest API to log batches of items
        :type endpoint: str
        """

        try:
            # Prepare the body of the request with the information to track
            items_to_track = []
            for key, value in data.items():
                item_to_track = {"key": key, "value": value}
                items_to_track.append(item_to_track)

            body = {
                "run_id": self.run_id,
                item_type: items_to_track
            }
            # Launch the post request to track the information in the experiment run
            self.post(endpoint=endpoint, body=body)
        except Exception as err:
            message = (f'Error tracking {item_type} in a MLflow experiment run using the '
                       f'MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)
