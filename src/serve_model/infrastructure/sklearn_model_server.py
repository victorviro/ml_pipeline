import logging

import pandas as pd
import mlflow
from mlflow.tracking import MlflowClient

from src.transform_data.infrastructure.sklearn_data_transformer import (
    SklearnDataTransformer)
from src.transform_data.application.transform_data_use_case import transform_data
from src.shared.constants import TRANSFORMER_PIPELINE_NAME, REGISTRY_MODEL_NAME
from src.shared.files_helper import load_pickle_file


logger = logging.getLogger(__name__)


class SklearnModelServer():

    def __init__(self, raw_data: dict):
        self.raw_data = raw_data
        self.sklearn_data_transformer = SklearnDataTransformer()
        self.model, self.transformer_pipeline = self.get_model_and_transformer_pipe()

    def serve_predictions(self):
        # Transform data and make predictions
        transformed_data = transform_data(self.sklearn_data_transformer, self.raw_data,
                                          self.transformer_pipeline)
        data_df = pd.DataFrame.from_dict(transformed_data)
        predictions = self.model.predict(data_df)
        return predictions

    def get_model_and_transformer_pipe(self):
        # Load the last model registered in MLflow model registry stagged as Staging
        try:
            client = MlflowClient()
            # Get info of the last staged model in MLflow model registry
            registered_models = client.get_latest_versions(REGISTRY_MODEL_NAME,
                                                           stages=["Staging"])
            version_model_registered = registered_models[0].version
            logger.info(f'Registered model version: {version_model_registered}')
            # Load the model
            model_uri = f'models:/{REGISTRY_MODEL_NAME}/{version_model_registered}'
            model = mlflow.sklearn.load_model(model_uri=model_uri)
            logger.info('Model trained loaded from MLflow registry sucessfully. Model '
                        f'name: {REGISTRY_MODEL_NAME}; '
                        f'version: {version_model_registered}')
            artifacts_path = registered_models[0].source
            # Load the sklearn transformer pipeline
            transformer_pipe_path = f'{artifacts_path}/{TRANSFORMER_PIPELINE_NAME}.pkl'
            transformer_pipeline = load_pickle_file(transformer_pipe_path)
            return model, transformer_pipeline
        except Exception as err:
            msg = ('Error loading the model trained from MLflow registry.'
                   f' Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
