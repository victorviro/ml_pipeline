import logging

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import mlflow
from mlflow.tracking import MlflowClient

from src.shared.files_helper import get_json_from_file_path, load_pickle_file
from src.shared.training_helper import get_regression_metrics
from src.shared.constants import REGISTRY_MODEL_NAME


logger = logging.getLogger(__name__)


class SklearnModelValidator():
    """
    A class which implements the interface IModelValidator to validate the model.
    It validates the model if the root mean squared error (rmse) in the test set
    is smaller than a value given. If the model is validated, its stage is updated
    to 'Staging' in MLflow registry.

    :param transformed_data_path: Path where the preprocessed data is stored
    :type transformed_data_path: str
    :param data_name: Name of the dataset
    :type data_name: str
    :param rmse_threshold: Threshold to validate the model using the rmse
    :type rmse_threshold: float
    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int

    """
    def __init__(self, transformed_data_path: str, data_name: str, rmse_threshold: float,
                 size_test_split: float, test_split_seed: int):
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.rmse_threshold = rmse_threshold
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def validate_model(self):

        logger.info(f'Validating model')

        # Get data and convert to pandas DataFrame
        try:
            data = get_json_from_file_path(self.full_transformed_data_path)
            logger.info(f'Loaded data succesfully.')
            data_df = pd.DataFrame.from_dict(data)
        except Exception as err:
            msg = f'Error loading data or converting it to df. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Split the data into training and test sets.
        try:
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
        except Exception as err:
            msg = f'Error getting target variable or splitting data. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Load the trained model, make predictions and compute metrics on the test set
        try:
            # Load the last model registered in MLflow model registry stagged as None
            client = MlflowClient()
            registered_models = client.get_latest_versions(REGISTRY_MODEL_NAME,
                                                           stages=["None"])
            version_model_registered = registered_models[0].version
            logger.info(f'Registered model version: {version_model_registered}')
            model_uri = f'models:/{REGISTRY_MODEL_NAME}/{version_model_registered}'
            model = mlflow.sklearn.load_model(model_uri=model_uri)
            y_test_predicted = model.predict(X_test)
            (rmse, mae, r2) = get_regression_metrics(y_test, y_test_predicted)
        except Exception as err:
            msg = ('Error loading the model trained in pkl format or getting predictions'
                   f' or getting metrics on test set. Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)

        logger.info(f'Metrics: \nRMSE: {rmse} \nMAE: {mae} \nR2: {r2}')

        if rmse > self.rmse_threshold:
            msg = ('Square root of mean squared error bigger that the thresold fixed:'
                   f' {rmse} > thresold fixed = {self.rmse_threshold}')
            raise Exception(f'Model was not validated succesfully in test set: {msg}')
        else:
            msg = ('Square root of mean squared error smaller that the thresold fixed:'
                   f' {rmse} < thresold fixed = {self.rmse_threshold}')
            logger.info(f'Model validated succesfully in test set: {msg}')
            # Update the stage of the model to "Staging" in MLflow model registry
            client.transition_model_version_stage(
                    name=REGISTRY_MODEL_NAME,
                    version=version_model_registered,
                    stage="Staging"
            )
            logger.info('Updated stage of model registered in MLflow registry to Staging.'
                        f' Name: {REGISTRY_MODEL_NAME}. '
                        f'Version: {version_model_registered}')
