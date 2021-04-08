from json import dumps, loads
from requests import post, get
import logging
from os import getcwd
from time import time

from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.constants import (MODEL_NAME, MLFLOW_API_ENDPOINT_GET_RUN,
                                  MLFLOW_API_ENDPOINT_SEARCH_MODEL_VERSIONS,
                                  REGISTRY_MODEL_NAME,
                                  MLFLOW_API_ENDPOINT_UPDATE_MODEL_STAGE,
                                  MLFLOW_API_URI, MLFLOW_API_ENDPOINT_LOG_BATCH,
                                  MLFLOW_API_ENDPOINT_LATEST_MODEL_VERSION,
                                  MLFLOW_API_ENDPOINT_GET_EXPERIMENT_BY_NAME,
                                  MLFLOW_API_ENDPOINT_CREATE_RUN)


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
    def __init__(self, run_id: str = None):
        self.run_id = run_id
        self.base_url = MLFLOW_API_URI

    def track_data(self):
        return NotImplementedError

    def launch_request(self, endpoint: str, body: dict, request_type: str):
        """
        Launch a POST request (to track information).

        :param endpoint: The endpoint of the MLflow Rest API for the specific case
        :type endpoint: str
        :param body: The body of the request
        :type body: dict
        :param request_type: The type of the request (post/get)
        :type request_type: str
        """
        url = f'{self.base_url}/{endpoint}'
        # Track the information through a request
        try:
            if request_type == 'post':
                request = post(url, data=dumps(body))
                message = 'Tracked experiment information in MLflow succesfully.'
            if request_type == 'get':
                request = get(url, data=dumps(body))
                message = 'Gotten experiment information from MLflow succesfully.'

            if request.status_code == 200:
                logger.info(f'{message} Run id: {self.run_id}')
                return request
            else:
                msg = (f'Request {request_type} error: Status code: {request.status_code}'
                       f'. Content: {request.content}')
                raise Exception(msg)

        except Exception as err:
            message = ('Error tracking/getting experiment information using the MLflow '
                       f'Rest Api. \nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def track_items(self, data: dict, item_type: str):
        """
        Track items (params, metrics or tags) into an MLflow experiment run.

        :param data: The data information to track
        :type data: dict
        :param item_type: The type of items to track (tags/metrics/params)
        :type item_type: str
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
            self.launch_request(endpoint=MLFLOW_API_ENDPOINT_LOG_BATCH, body=body,
                                request_type='post')
        except Exception as err:
            message = (f'Error tracking {item_type} in a MLflow experiment run using the '
                       f'MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def get_artifacts_path(self) -> str:
        """
        Get artifacts path into an MLflow experiment run.

        :return: The artifacts path
        :rtype: str
        """
        try:
            # Prepare the body of the request
            body = {"run_id": self.run_id}
            # Launch the get request to get the information of the experiment run
            request = self.launch_request(endpoint=MLFLOW_API_ENDPOINT_GET_RUN, body=body,
                                          request_type='get')
            content = loads(request.content.decode('utf-8'))
            artifact_uri = content["run"]["info"]["artifact_uri"]
            artifacts_path = f'{getcwd()}/{artifact_uri}/{MODEL_NAME}'
            return artifacts_path
        except Exception as err:
            message = (f'Error getting info (artifacts path) of a MLflow experiment run '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def search_model_version(self) -> str:
        """
        Get the model version of a run registered in MLFLOW Registry.

        :return: The model version
        :rtype: str
        """
        try:
            # Prepare the body of the request
            body = {"filter": f"run_id='{self.run_id}'"}
            # Launch the request to get the model version of the run
            request = self.launch_request(
                endpoint=MLFLOW_API_ENDPOINT_SEARCH_MODEL_VERSIONS,
                body=body, request_type='get'
            )
            content = loads(request.content.decode('utf-8'))
            version_model_registered = content["model_versions"][0]["version"]
            return version_model_registered
        except Exception as err:
            message = (f'Error getting model version of a run in MLflow Registry '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def transition_model_version_stage(self, stage: str):
        """
        Update model version stage in MLflow Registry.

        :param stage: New desired stage for this model version (None/staging/production)
        :type stage: str
        """
        # Get the version of the model registered
        version_model_registered = self.search_model_version()
        try:
            # Prepare the body of the request
            body = {
                "name": REGISTRY_MODEL_NAME,
                "version": version_model_registered,
                "stage": stage
            }
            # Launch the request to update model version stage
            self.launch_request(
                endpoint=MLFLOW_API_ENDPOINT_UPDATE_MODEL_STAGE,
                body=body, request_type='post'
            )
            logger.info('Updated stage of model registered in MLflow registry to '
                        f'{stage}. Name: {REGISTRY_MODEL_NAME}. '
                        f'Version: {version_model_registered}')
        except Exception as err:
            message = (f'Error updating stage of model {REGISTRY_MODEL_NAME} version '
                       f'{version_model_registered} in MLflow Registry '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def get_artifacts_path_of_latest_model_version(self, name: str, stage: str) -> str:
        """
        Get the path of the artifacts stored in the latest model version in stage
        "Staging" from MLflow Model Registry.

        :param name: The registered model name
        :type name: str
        :param stage: The stage of the model version in MLflow Model Registry
        :type stage: str
        :return: The artifacts path
        :rtype: str
        """
        try:
            # Prepare the body of the request
            body = {
                "name": name,
                "stages": [stage]
            }
            # Launch the request to get info of latest model versions
            request = self.launch_request(
                endpoint=MLFLOW_API_ENDPOINT_LATEST_MODEL_VERSION,
                body=body, request_type='get'
            )
            content = loads(request.content.decode('utf-8'))
            relative_artifacts_path = content["model_versions"][0]["source"]
            artifact_paths = f'{getcwd()}/{relative_artifacts_path}'
            version_model_registered = content["model_versions"][0]["version"]
            logger.info('Gotten info of the latest model registered in MLflow registry'
                        f' with stage {stage}. Name: {name}. '
                        f'Version: {version_model_registered}')
            return artifact_paths
        except Exception as err:
            message = (f'Error getting info of the latest model registered in MLflow '
                       f'Registry with stage {stage}, name: {name}, '
                       f'version {version_model_registered}, '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def get_experiment_id_by_name(self, experiment_name: str) -> str:
        """
        Get the experiment id given the experiment name.

        :param experiment_name: The name of the experiment
        :type experiment_name: str
        :return: The id of the experiment
        :rtype: str
        """
        try:
            # Prepare the body of the request
            body = {"experiment_name": experiment_name}
            # Launch the request to get the experiment info
            request = self.launch_request(
                endpoint=MLFLOW_API_ENDPOINT_GET_EXPERIMENT_BY_NAME,
                body=body, request_type='get'
            )
            content = loads(request.content.decode('utf-8'))
            experiment_id = content["experiment"]["experiment_id"]
            return experiment_id
        except Exception as err:
            message = (f'Error getting the experiment id by an experiment name '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def create_run_by_experiment_id(self, experiment_id: str) -> str:
        """
        Create a run of an experiment given the experiment id.

        :param experiment_id: The id of the experiment
        :type experiment_id: str
        :return: The id of the run created
        :rtype: str
        """
        try:
            # Prepare the body of the request
            body = {
                "experiment_id": experiment_id,
                "start_time": round(time() * 1000)
            }
            # Launch the request to get the experiment info
            request = self.launch_request(
                endpoint=MLFLOW_API_ENDPOINT_CREATE_RUN,
                body=body, request_type='post'
            )
            content = loads(request.content.decode('utf-8'))
            run_id = content["run"]["info"]["run_id"]
            return run_id
        except Exception as err:
            message = (f'Error creating a run in experiment with id {experiment_id} '
                       f'using the MLflow Rest Api.\nTraceback of error: {str(err)}')
            logger.error(message)
            raise Exception(message)

    def create_run_by_experiment_name(self, experiment_name: str) -> str:
        """
        Create a run of an experiment given the experiment name.

        :param experiment_name: The name of the experiment
        :type experiment_name: str
        :return: The id of the run created
        :rtype: str
        """
        # Get the experiment id by experiment name
        experiment_id = self.get_experiment_id_by_name(experiment_name)
        # Create a run of the experiment given the experiment id
        run_id = self.create_run_by_experiment_id(experiment_id=experiment_id)
        return run_id
