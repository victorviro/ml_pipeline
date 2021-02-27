import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
import dvc.api
import mlflow
import mlflow.sklearn

from src.config_variables import (RAW_DATA_PATH, MCPL_TEST_SPLIT, TRAIN_MODEL_EXP_NAME,
                                  PROJECT_PATH, VERSION, ARTIFACT_LOCAL_PATH,
                                  MLFLOW_TRACKING_URI, TEST_SPLIT_SEED, MODEL_SEED)
from src.utils.files import get_json_from_file_path
from src.utils.training import get_regression_metrics

logger = logging.getLogger(__name__)


class MlflowSklearnTrainer:
    def __init__(self, raw_data_path: str, transformed_data_path: str, data_name: str,
                 alpha: float, l1_ratio: float):
        self.raw_data_path = raw_data_path
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.full_raw_data_path = f'{raw_data_path}/{data_name}.json'
        self.alpha = alpha
        self.l1_ratio = l1_ratio

    def train_model(self):

        logger.info('Training the model for MCPL prediction. Dataset name:'
                    f' {self.data_name}')
        # Get data
        try:
            data = get_json_from_file_path(self.full_transformed_data_path)
            logger.info(f'Loaded data succesfully.')
        except Exception as err:
            msg = f'Error loading data. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        # Load data to pandas DataFrame and transform it
        try:
            data_df = pd.DataFrame.from_dict(data)
        except Exception as err:
            msg = f'Error converting dict data to pandas df. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        # The target variable is "max_char_per_line"
        try:
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
        except Exception as err:
            msg = f'Error getting target variable in pandas df. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Split the data into training and test sets.
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=MCPL_TEST_SPLIT, random_state=TEST_SPLIT_SEED
        )
        logger.info(f'X_train shape: {X_train.shape}')
        logger.info(f'X_test shape: {X_test.shape}')

        # Set MLflow URI
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        except Exception as err:
            msg = (f'Error setting MLflow URI: {MLFLOW_TRACKING_URI}. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Set MLflow experiment
        try:
            mlflow.set_experiment(experiment_name=TRAIN_MODEL_EXP_NAME)
        except Exception as err:
            msg = (f'Error setting MLflow experiment with name: {TRAIN_MODEL_EXP_NAME}. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Start a MLflow run
        try:
            with mlflow.start_run():

                # Define the model
                model = ElasticNet(alpha=self.alpha, l1_ratio=self.l1_ratio,
                                   random_state=MODEL_SEED)
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
                mlflow.log_param("test_split_seed", TEST_SPLIT_SEED)
                mlflow.log_param("model_seed", MODEL_SEED)
                mlflow.log_param("test_split_percent", MCPL_TEST_SPLIT)
                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)
                dvc_raw_data_path = dvc.api.get_url(path=self.full_raw_data_path,
                                                    repo=PROJECT_PATH)
                mlflow.set_tag("dvc_raw_data_path", dvc_raw_data_path)
                mlflow.set_tag("version", VERSION)

                # Serialize the model in a format that MLflow knows how to deploy it
                mlflow.sklearn.log_model(model, ARTIFACT_LOCAL_PATH)
                # Get the relative path of the artifact (artifact_store/123../artifacts)
                artifact_uri = mlflow.get_artifact_uri()
                return artifact_uri

        except Exception as err:
            msg = (f'Error starting MLflow experiment or withing the experiment. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
