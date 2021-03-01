import logging
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import dvc.api
import mlflow
import mlflow.sklearn

from src.config_variables import (TRAIN_MODEL_EXPERIMENT_NAME, MLFLOW_TRACKING_URI)
from src.utils.files import get_json_from_file_path, save_pickle_file
from src.utils.training import get_regression_metrics

logger = logging.getLogger(__name__)


class MlflowSklearnTrainer:
    def __init__(self, raw_data_path: str, transformed_data_path: str, data_name: str,
                 alpha: float, l1_ratio: float, version: int, model_path: str,
                 model_name: str, size_test_split: float, test_split_seed: int,
                 model_seed: int):
        self.raw_data_path = raw_data_path
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.full_raw_data_path = f'{raw_data_path}/{data_name}.json'
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.version = version
        self.model_name = model_name
        self.full_model_path = f'{model_path}/{model_name}.pkl'
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.model_seed = model_seed

    def train_model(self):

        logger.info('Training the model for MCPL prediction. Dataset name:'
                    f' {self.data_name}')
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

        # Set MLflow URI (todo env variable)
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        except Exception as err:
            msg = (f'Error setting MLflow URI: {MLFLOW_TRACKING_URI}. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Set MLflow experiment (todo env variable)
        try:
            mlflow.set_experiment(experiment_name=TRAIN_MODEL_EXPERIMENT_NAME)
        except Exception as err:
            msg = ('Error setting MLflow experiment with name: '
                   f'{TRAIN_MODEL_EXPERIMENT_NAME}. Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Start a MLflow run
        try:
            with mlflow.start_run():

                # Define the model
                model = ElasticNet(alpha=self.alpha, l1_ratio=self.l1_ratio,
                                   random_state=self.model_seed)
                # Train the model
                model.fit(X_train, y_train)

                # Predictions in the test set
                y_test_predicted = model.predict(X_test)

                # Compute metrics in the test data
                (rmse, mae, r2) = get_regression_metrics(y_test, y_test_predicted)

                logger.info(f'Model trained: alpha={self.alpha}, '
                            f'l1_ratio={self.l1_ratio}.')
                logger.info(f'Metrics: \nRMSE: {rmse} \nMAE: {mae} \nR2: {r2}')

                # Track information in MLflow (hyperparameters, metrics...)
                mlflow.log_param("alpha", self.alpha)
                mlflow.log_param("l1_ratio", self.l1_ratio)
                mlflow.log_param("test_split_seed", self.test_split_seed)
                mlflow.log_param("model_seed", self.model_seed)
                mlflow.log_param("test_split_percent", self.size_test_split)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                # Get and track the path of the dataset in the DVC repository
                dvc_raw_data_path = dvc.api.get_url(path=self.full_raw_data_path,
                                                    repo=os.getcwd())
                mlflow.set_tag("dvc_raw_data_path", dvc_raw_data_path)
                mlflow.set_tag("version", self.version)
                mlflow.set_tag("model_path", self.full_model_path)
                mlflow.set_tag("raw_data_path", self.full_raw_data_path)

                # Serialize the model in a format that MLflow knows how to deploy it
                mlflow.sklearn.log_model(model, self.model_name)
                # Save the model in /models/
                save_pickle_file(file_path=self.full_model_path, file=model)

        except Exception as err:
            msg = (f'Error starting MLflow experiment or withing the experiment. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
