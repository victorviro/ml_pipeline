import logging
import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from hpsklearn import HyperoptEstimator
from hpsklearn import any_regressor
from hpsklearn import any_preprocessing
import hpsklearn
from hyperopt import tpe, hp
import mlflow
import dvc.api

from src.utils.files import get_json_from_file_path
from src.utils.training import get_regression_metrics, get_class_parameters
from src.config_variables import MLFLOW_TRACKING_URI, HYPER_PARAMETER_EXP_NAME


logger = logging.getLogger(__name__)


class HyperoptHyperparameterOptimizer:
    def __init__(self, raw_data_path: str, transformed_data_path: str, data_name: str,
                 version: int, model_path: str,
                 model_name: str, size_test_split: float, test_split_seed: int,
                 model_seed: int):
        self.raw_data_path = raw_data_path
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.full_raw_data_path = f'{raw_data_path}/{data_name}.json'
        self.version = version
        self.model_name = model_name
        self.full_model_path = f'{model_path}/{model_name}.pkl'
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.model_seed = model_seed
        self.hyperopt_max_evals = hyperopt_max_evals

    def optimize_hyperparameters(self):

        logger.info(f'Hyper-parameter optimization. Dataset name: {data_name}')

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
            mlflow.set_experiment(experiment_name=HYPER_PARAMETER_EXP_NAME)
        except Exception as err:
            msg = (f'Error setting MLflow experiment with name: {TRAIN_MODEL_EXP_NAME}. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
        # Start a MLflow run
        try:
            with mlflow.start_run():

                # Define the type of regressor algorithms to do the the search
                regressors = hp.choice(
                    'mcpl_prediction',
                    [hpsklearn.elasticnet('mcpl_prediction.elasticnet')]
                    # hpsklearn.random_forest_regression(), hpsklearn.svc(''),
                )

                # We define the search procedure.
                # We will explore the regressor above and all data transforms available
                hyperopt_estimator = HyperoptEstimator(
                                        regressor=regressors,  # any_regressor('reg'),
                                        preprocessing=any_preprocessing('pre'),
                                        # [hpsklearn.standard_scaler('standard_scaler')]
                                        loss_fn=mean_squared_error,
                                        algo=tpe.suggest,
                                        max_evals=self.hyperopt_max_evals,
                                        trial_timeout=30)

                hyperopt_estimator.fit(X_train, y_train)

                # Performance
                y_test_predicted = hyperopt_estimator.predict(X_test)
                (rmse_test, r2_test, mae_test) = get_regression_metrics(
                    y_test, y_test_predicted
                )
                # Track metrics in MLflow
                mlflow.log_metric("rmse_test", rmse_test)
                mlflow.log_metric("r2_test", r2_test)
                mlflow.log_metric("mae_test", mae_test)

                y_train_predicted = hyperopt_estimator.predict(X_train)
                (rmse_train, r2_train, mae_train) = get_regression_metrics(
                    y_train, y_train_predicted
                )
                # Track metrics in MLflow
                mlflow.log_metric("rmse_train", rmse_train)
                mlflow.log_metric("r2_train", r2_train)
                mlflow.log_metric("mae_train", mae_train)

                # Get the info of the best model choosen
                best_model_info = hyperopt_estimator.best_model()
                # Get the best regressor choosen
                best_regressor = best_model_info["learner"]
                logger.info(f'\nBest regressor:{best_regressor}')
                # Get the name of the regressor and the name of its parameters
                regressor_name = best_regressor.__class__.__name__
                regressor_param_names = get_class_parameters(best_regressor)
                # Get the best prepocessing method choosen
                best_preprocessing = best_model_info["preprocs"][0]
                logger.info(f'\nBest preprocessing:{best_preprocessing}')
                # Get the name of the prepocessing method and the name of its parameters
                preprocessing_name = best_preprocessing.__class__.__name__
                preprocessing_param_names = get_class_parameters(best_preprocessing)

                # Track params in MLflow
                mlflow.set_tag("regressor name", regressor_name)
                for regressor_param_name in regressor_param_names:
                    param_value = getattr(best_regressor, regressor_param_name)
                    param_name = f'regressor_{regressor_param_name}'
                    mlflow.log_param(param_name, param_value)

                mlflow.set_tag("preprocessing name", preprocessing_name)
                for preprocessing_param_name in preprocessing_param_names:
                    param_value = getattr(best_preprocessing, preprocessing_param_name)
                    param_name = f'preprocessing_{preprocessing_param_name}'
                    mlflow.log_param(param_name, param_value)

                mlflow.set_tag("version", self.version)
                data_path = dvc.api.get_url(path=data_file_path, repo=os.getcwd())
                mlflow.set_tag("data path", data_path)
                mlflow.log_param("test_split_percent", self.size_test_split)
                mlflow.log_param("test_split_seed", self.test_split_seed)

        except Exception as err:
            msg = (f'Error starting MLflow experiment or withing the experiment. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)
