import json
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
    :param key: The key to track (tags/metrics/params)
    :type key: str
    :param url: The url of the MLflow Rest API to track batches of items
    :type url: str
    """
    def __init__(self, run_id: str, key: str, url: str):
        self.run_id = run_id
        self.key = key
        self.url = url

    def track_data(self, data: dict):
        """
        Track data into an MLflow experiment using requests to the MLflow Rest API.

        :param data: The data information to track
        :type data: dict
        """
        # Prepare the body of the request with the information to track
        items_to_track = []
        for key, value in data.items():
            item_to_track = {"key": key, "value": value}
            items_to_track.append(item_to_track)

        body = {
            "run_id": self.run_id,
            self.key: items_to_track
        }
        # Track the information through a request
        try:
            request = requests.post(self.url, data=json.dumps(body))
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
