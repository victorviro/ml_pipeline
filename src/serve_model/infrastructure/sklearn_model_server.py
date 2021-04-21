import logging
from os import getcwd
from requests import post
from json import loads, dumps

from pandas import DataFrame
from numpy import ndarray

from src.shared.constants import (TRANSFORMER_PIPELINE_NAME, REGISTRY_MODEL_NAME,
                                  MODEL_NAME)
from src.serve_model.domain.model_server import IModelServer
from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.data_file_loader import IDataFileLoader


logger = logging.getLogger(__name__)


class SklearnModelServer(IModelServer):
    """
    A class which implements the interface IModelServer to serve the model.
    """

    def serve_predictions(self, data: dict, data_tracker: IDataTracker,
                          model_file_loader: IDataFileLoader) -> ndarray:
        """
        Serve a model to make preditions.

        :param data: The data to be fed to the model to make predictions
        :type data: dict
        :param data_tracker: A data tracker to track info of the experiment
        :type data_tracker: IDataTracker
        :param model_file_loader: A data loader to load the model trained
        :type model_file_loader: IDataFileLoader
        :return: The prediction/s made by the model
        :rtype: numpy.ndarray
        """
        # Get the path of the artifacts stored in the latest model version "Staged"
        artifacts_path = data_tracker.get_artifacts_path_of_latest_model_version(
            name=REGISTRY_MODEL_NAME,
            stage='Staging'
        )
        try:
            # Load the model
            model_path = f'{artifacts_path}/{MODEL_NAME}.pkl'
            model = model_file_loader.load_data(file_path=model_path)
            logger.info('Model trained loaded from MLflow registry sucessfully')
        except Exception as err:
            msg = ('Error loading the model trained from MLflow registry.'
                   f' Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Transform data
        try:
            body = {
                "transformer_pipe_path": artifacts_path,
                "pipe_name": TRANSFORMER_PIPELINE_NAME,
                "data": data
            }
            request = post('', data=dumps(body))
            content = loads(request.content.decode('utf-8'))
            data_df = DataFrame(content["data"])
            logger.info(f'Data transfomerd succesfully')
        except Exception as err:
            msg = f'Error transforming features. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Make predictions
        try:
            predictions = model.predict(data_df)
            logger.info('Predictions made by the model succesfully.')
            return predictions
        except Exception as err:
            msg = f'Error making predictions. Error: {err}'
            logger.error(msg)
            raise Exception(msg)
