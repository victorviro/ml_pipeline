import logging
from os import getcwd
import json
import requests

from pandas import DataFrame
from sklearn.model_selection import train_test_split
import mlflow
from mlflow.tracking import MlflowClient

from src.shared.training_helper import get_regression_metrics
from src.shared.constants import (REGISTRY_MODEL_NAME, URL_TRANSFORM_DATA_API,
                                  TRANSFORMER_PIPELINE_NAME)
from src.validate_model.domain.model_validator import IModelValidator


logger = logging.getLogger(__name__)


class SklearnModelValidator(IModelValidator):
    """
    A class which implements the interface IModelValidator to validate the model.
    It validates the model if the root mean squared error (rmse) in the test set
    is smaller than a value given. If the model is validated, its stage is updated
    to 'Staging' in MLflow registry.
    """

    def validate_model(self, data: dict, rmse_threshold: float, size_test_split: float,
                       test_split_seed: int):
        """
        Validate the model if the root mean squared error (rmse) in the test set
        is smaller than a value given. If the model is validated, its stage is updated
        to 'Staging' in MLflow registry.

        :param data: The dataset used to validate the model (before splitting it)
        :type data: dict
        :param rmse_threshold: Threshold to validate the model using the rmse
        :type rmse_threshold: float
        :param size_test_split: Percentage of test dataset when splitting the dataset
        :type size_test_split: float
        :param test_split_seed: Seed used when splitting the dataset
        :type test_split_seed: int
        """

        logger.info(f'Validating model')

        # Convert dataset to pandas DataFrame
        try:
            data_df = DataFrame.from_dict(data)
            logger.info(f'Dataset converted to pandas DataFrame succesfully.')
        except Exception as err:
            msg = f'Error loading data or converting it to df. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Split the data into training and test sets.
        try:
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=size_test_split, random_state=test_split_seed
            )
        except Exception as err:
            msg = f'Error getting target variable or splitting data. Error: {err}'
            logger.error(msg)
            raise Exception(msg)
        # Get info of the experiment from MLflow
        try:
            client = MlflowClient()
            # Get info of the last model registered in MLflow Registry stagged as None
            registered_models = client.get_latest_versions(REGISTRY_MODEL_NAME,
                                                           stages=["None"])
            version_model_registered = registered_models[0].version
            logger.info(f'Registered model version: {version_model_registered}')
            relative_model_path = registered_models[0].source
        except Exception as err:
            msg = f'Error getting info of experiment in MLflow. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Transform test features.
        try:
            body = {
                "transformer_pipe_path": f'{getcwd()}/{relative_model_path}',
                "pipe_name": TRANSFORMER_PIPELINE_NAME
            }
            # Transform test features
            body.update({"data": X_test.to_dict(orient='list')})
            request = requests.post(URL_TRANSFORM_DATA_API, data=json.dumps(body))
            content = json.loads(request.content.decode('utf-8'))
            X_test = DataFrame(content["data"])
        except Exception as err:
            msg = f'Error transforming test features. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Load the trained model, make predictions and compute metrics on the test set
        try:
            # Load the model registered in MLflow
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

        if rmse > rmse_threshold:
            msg = ('Square root of mean squared error bigger that the thresold fixed:'
                   f' {rmse} > thresold fixed = {rmse_threshold}')
            raise Exception(f'Model was not validated succesfully in test set: {msg}')
        else:
            msg = ('Square root of mean squared error smaller that the thresold fixed:'
                   f' {rmse} < thresold fixed = {rmse_threshold}')
            logger.info(f'Model validated succesfully in test set: {msg}')
            try:
                # Update the stage of the model to "Staging" in MLflow model registry
                client.transition_model_version_stage(
                        name=REGISTRY_MODEL_NAME,
                        version=version_model_registered,
                        stage="Staging"
                )
                logger.info('Updated stage of model registered in MLflow registry to '
                            f'Staging. Name: {REGISTRY_MODEL_NAME}. '
                            f'Version: {version_model_registered}')
            except Exception as err:
                msg = ('Error updating the model"s stage in MLflow Registry to "Stagging"'
                       f'. Traceback of error: {err}')
                logger.error(msg)
                raise Exception(msg)
