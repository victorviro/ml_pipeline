import logging
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import dvc.api
import mlflow
import mlflow.sklearn

from src.shared.constants import TRAIN_MODEL_EXPERIMENT_NAME, REGISTRY_MODEL_NAME
from src.shared.files_helper import (get_json_from_file_path, save_pickle_file,
                                     load_pickle_file)
from src.shared.training_helper import get_regression_metrics


logger = logging.getLogger(__name__)


class MlflowSklearnTrainer:
    def __init__(self, raw_data_path: str, transformed_data_path: str, data_name: str,
                 alpha: float, l1_ratio: float, version: int, model_path: str,
                 transformer_name: str, model_name: str, size_test_split: float,
                 test_split_seed: int, model_seed: int):
        self.raw_data_path = raw_data_path
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.full_raw_data_path = f'{raw_data_path}/{data_name}.json'
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.version = version
        self.transformer_name = transformer_name
        self.model_name = model_name
        self.full_transformer_path = f'{model_path}/{transformer_name}.pkl'
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

        try:
            mlflow.set_experiment(experiment_name=TRAIN_MODEL_EXPERIMENT_NAME)
        except Exception as err:
            msg = ('Error setting MLflow experiment with name: '
                   f'{TRAIN_MODEL_EXPERIMENT_NAME}. Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Start a MLflow run
        try:
            with mlflow.start_run() as run:

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
                mlflow.set_tag("raw_data_path", self.full_raw_data_path)

                # Track the model and transformer pipeline in MLflow
                mlflow.sklearn.log_model(sk_model=model, artifact_path=self.model_name)
                mlflow.log_artifact(local_path=self.full_transformer_path,
                                    artifact_path=self.model_name)

                model_artifact_uri = mlflow.get_artifact_uri(self.model_name)
                logger.info("Model artifact uri: {}".format(model_artifact_uri))
                # Track in MLflow name of steps of the transformer pipe in a dict
                transformer_pipe = load_pickle_file(self.full_transformer_path)
                transformer_steps = {'transformer_steps': [*transformer_pipe.named_steps]}
                mlflow.log_dict(transformer_steps, 'transformer_pipe.json')

                # Register the model in MLflow registry (staged as None)
                model_uri = f'runs:/{run.info.run_id}/{self.model_name}'
                registered_model_info = mlflow.register_model(model_uri=model_uri,
                                                              name=REGISTRY_MODEL_NAME)
                # Get the version of the model registered in MLflow registry
                version_model_registered = registered_model_info.version
                logger.info('Model registered in MLflow registry. Name: '
                            f'{REGISTRY_MODEL_NAME}. Version: {version_model_registered}')

                tracking_uri = mlflow.get_tracking_uri()
                logger.info("Current tracking uri: {}".format(tracking_uri))

        except Exception as err:
            msg = (f'Error starting MLflow experiment or within the experiment. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
