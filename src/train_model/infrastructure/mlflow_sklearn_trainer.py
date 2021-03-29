import logging
from os import getcwd
import requests
import json

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from dvc.api import get_url
import mlflow
import mlflow.sklearn

from src.shared.constants import (TRAIN_MODEL_EXPERIMENT_NAME, REGISTRY_MODEL_NAME,
                                  URL_TRANSFORM_DATA_API)
from src.shared.files_helper import (get_json_from_file_path)
from src.shared.training_helper import get_regression_metrics


logger = logging.getLogger(__name__)


class MlflowSklearnTrainer:
    """
    A class which implements the interface IModelTrainer to train a model.
    It trains the model using Scikit-learn, track the experiment in MLFlow, and
    register the model trained in MLFlow model registry.

    :param raw_data_path: Path where the raw data is stored
    :type data_path: str
    :param data_name: Name of the dataset
    :type data_name: str
    :param alpha: Alpha hyperparameter of the elasticnet model
    :type alpha: float
    :param l1_ratio: L1 ratio hyperparameter of the elasticnet model
    :type l1_ratio: float
    :param version: Version of the data
    :type version: int
    :param transformer_pipe_path: Path where the transformer pipeline is stored
    :type transformer_pipe_path: str
    :param transformer_name: Name of the transformer pipeline stored
    :type transformer_name: str
    :param model_name: Name of the model used to track the experiment in MLFlow
    :type model_name: str
    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    :param model_seed: Seed used when training the model
    :type model_seed: int
    """
    def __init__(self, raw_data_path: str, data_name: str,
                 alpha: float, l1_ratio: float, version: int, transformer_pipe_path: str,
                 transformer_name: str, model_name: str, size_test_split: float,
                 test_split_seed: int, model_seed: int):

        self.raw_data_path = raw_data_path
        self.data_name = data_name
        self.full_raw_data_path = f'{raw_data_path}/{data_name}.json'
        self.alpha = alpha
        self.l1_ratio = l1_ratio
        self.version = version
        self.transformer_pipe_path = transformer_pipe_path
        self.transformer_name = transformer_name
        self.model_name = model_name
        self.full_transformer_path = f'{transformer_pipe_path}/{transformer_name}.pkl'
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.model_seed = model_seed

    def train_model(self):

        logger.info('Training the model for MCPL prediction. Dataset name:'
                    f' {self.data_name}')
        # Get data and convert to pandas DataFrame
        try:
            data = get_json_from_file_path(self.full_raw_data_path)
            logger.info(f'Loaded data succesfully.')
            data_df = DataFrame.from_dict(data)
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
        # Transform training and test features.
        try:
            body = {
                "transformer_pipe_path": self.transformer_pipe_path,
                "pipe_name": self.transformer_name
            }
            # Transform training features
            body.update({"data": X_train.to_dict(orient='list')})
            request = requests.post(URL_TRANSFORM_DATA_API, data=json.dumps(body))
            content = json.loads(request.content.decode('utf-8'))
            X_train = DataFrame(content["data"])
            # Transform test features
            body.update({"data": X_test.to_dict(orient='list')})
            request = requests.post(URL_TRANSFORM_DATA_API, data=json.dumps(body))
            content = json.loads(request.content.decode('utf-8'))
            X_test = DataFrame(content["data"])
        except Exception as err:
            msg = f'Error transforming train or test features. Error: {err}'
            logger.error(msg)
            raise Exception(msg)
        # Set experiment to track in MLFlow
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

                # Predictions in the test and training sets
                y_test_predicted = model.predict(X_test)
                y_train_predicted = model.predict(X_train)

                # Compute metrics in the test and training sets
                (rmse_test, mae_test, r2_test) = get_regression_metrics(y_test,
                                                                        y_test_predicted)
                (rmse_train, mae_train, r2_train) = get_regression_metrics(
                    y_train, y_train_predicted
                )

                logger.info(f'Model trained: alpha={self.alpha}, '
                            f'l1_ratio={self.l1_ratio}.')
                logger.info(f'Metrics train set: \nRMSE: {rmse_train} \nMAE: {mae_train}'
                            f' \nR2: {r2_train}')
                logger.info(f'Metrics test set: \nRMSE: {rmse_test} \nMAE: {mae_test}'
                            f' \nR2: {r2_test}')

                # Track information in MLflow (hyperparameters, metrics...)
                mlflow.log_param("alpha", self.alpha)
                mlflow.log_param("l1_ratio", self.l1_ratio)
                mlflow.log_param("test_split_seed", self.test_split_seed)
                mlflow.log_param("model_seed", self.model_seed)
                mlflow.log_param("test_split_percent", self.size_test_split)
                mlflow.log_metric("rmse_train", rmse_train)
                mlflow.log_metric("r2_train", r2_train)
                mlflow.log_metric("mae_train", mae_train)
                mlflow.log_metric("rmse_test", rmse_test)
                mlflow.log_metric("r2_test", r2_test)
                mlflow.log_metric("mae_test", mae_test)
                # Get and track in MLflow the path of the dataset in the DVC repository
                dvc_raw_data_path = get_url(path=self.full_raw_data_path,
                                            repo=getcwd())
                mlflow.set_tag("dvc_raw_data_path", dvc_raw_data_path)
                mlflow.set_tag("version", self.version)
                mlflow.set_tag("raw_data_path", self.full_raw_data_path)

                # Track the model and transformer pipeline in MLflow
                mlflow.sklearn.log_model(sk_model=model, artifact_path=self.model_name)
                mlflow.log_artifact(local_path=self.full_transformer_path,
                                    artifact_path=self.model_name)

                model_artifact_uri = mlflow.get_artifact_uri(self.model_name)
                logger.info("Model artifact uri: {}".format(model_artifact_uri))

                # Register the model in MLflow registry (staged as None)
                model_uri = f'runs:/{run.info.run_id}/{self.model_name}'
                registered_model_info = mlflow.register_model(model_uri=model_uri,
                                                              name=REGISTRY_MODEL_NAME)
                # Get the version of the model registered in MLflow registry
                version_model_registered = registered_model_info.version
                logger.info('Model registered in MLflow registry. Name: '
                            f'{REGISTRY_MODEL_NAME}. Version: {version_model_registered}')

                tracking_uri = mlflow.get_tracking_uri()
                logger.info(f'Current tracking uri: {tracking_uri}')

        except Exception as err:
            msg = (f'Error starting MLflow experiment or within the experiment. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
