import logging
from os import getcwd
import requests
import json

from pandas import DataFrame
from mlflow.sklearn import load_model
from mlflow.tracking import MlflowClient

from src.shared.constants import (TRANSFORMER_PIPELINE_NAME, REGISTRY_MODEL_NAME,
                                  URL_TRANSFORM_DATA_API)
from src.serve_model.domain.model_server import IModelServer


logger = logging.getLogger(__name__)


class SklearnModelServer(IModelServer):
    """
    A class which implements the interface IModelServer to serve the model.
    """

    def serve_predictions(self, data: dict):
        """
        Serve a model to make preditions.

        :param data: The data to be fed to the model to make predictions
        :type data: dict
        :return: The prediction/s made by the model
        :rtype: [type]
        """
        # Get info of the model
        model_info = self.get_model_info()
        # Load the model trained
        try:
            model_registered_version = model_info.version
            model_uri = f'models:/{REGISTRY_MODEL_NAME}/{model_registered_version}'
            model = load_model(model_uri=model_uri)
            logger.info('Model trained loaded from MLflow registry sucessfully. Model '
                        f'registry name: {REGISTRY_MODEL_NAME}; '
                        f'version: {model_registered_version}')
        except Exception as err:
            msg = ('Error loading the model trained from MLflow registry.'
                   f' Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Transform data
        try:
            relative_artifacts_path = model_info.source
            body = {
                "transformer_pipe_path": f'{getcwd()}/{relative_artifacts_path}',
                "pipe_name": TRANSFORMER_PIPELINE_NAME,
                "data": data
            }
            request = requests.post(URL_TRANSFORM_DATA_API, data=json.dumps(body))
            content = json.loads(request.content.decode('utf-8'))
            data_df = DataFrame(content["data"])
        except Exception as err:
            msg = f'Error transforming features. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Make predictions
        try:
            predictions = model.predict(data_df)
        except Exception as err:
            msg = f'Error making predictions. Error: {err}'
            logger.error(msg)
            raise Exception(msg)
        return predictions

    def get_model_info(self):
        # Get info of model registered in MLflow model registry stagged as Staging
        try:
            client = MlflowClient()
            # Get info of the last staged model in MLflow model registry
            registered_models = client.get_latest_versions(REGISTRY_MODEL_NAME,
                                                           stages=["Staging"])
            model_info = registered_models[0]
            return model_info
        except Exception as err:
            msg = ('Error getting info of the model from MLflow registry.'
                   f' Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
