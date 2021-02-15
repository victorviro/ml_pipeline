
import logging

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
from src.config_variables import (RAW_DATA_PATH, MCPL_TEST_SPLIT, VERSION, PROJECT_PATH,
                                  HYPER_PARAMETER_EXP_NAME, HYPEROPT_MAX_EVALS,
                                  MLFLOW_TRACKING_URI, TEST_SPLIT_SEED)


logger = logging.getLogger(__name__)


def hyper_parameter_search(data_name: str):
    """
    Track hyperpameter optimization in MLfLow.
    Hyperopt info: https://hyperopt.github.io/hyperopt-sklearn/

    :param data_name: Name of the dataset
    :type data_name: str
    """

    logger.info('======'*7)
    logger.info(f'Hyper-parameter optimization. Dataset name: {data_name}')

    # Load data to pandas DataFrame
    data_file_path = f'{RAW_DATA_PATH}/{data_name}.json'
    MCPL_dataset = get_json_from_file_path(data_file_path)
    MCPL_dataframe = pd.DataFrame.from_dict(MCPL_dataset)

    # The predicted column is "max_char_per_line"
    X = MCPL_dataframe.drop("max_char_per_line", axis=1)
    y = MCPL_dataframe["max_char_per_line"]

    X['ratio_cols_rows'] = X.cols_number/X.rows_number

    # Split the data into training and test sets.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=MCPL_TEST_SPLIT,
                                                        random_state=TEST_SPLIT_SEED)
    logger.info(f'X_train shape: {X_train.shape}')
    logger.info(f'X_test shape: {X_test.shape}')

    # Start a MLflow run
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(experiment_name=HYPER_PARAMETER_EXP_NAME)
    with mlflow.start_run():
        # Define the type of regressor algorithms to do the the search
        regressors = hp.choice('mcpl_prediction',
                               [hpsklearn.elasticnet('mcpl_prediction.elasticnet'),
                                # hpsklearn.random_forest_regression('mcpl_prediction.random_forest'),
                                # hpsklearn.svc('mcpl_prediction.svc'),
                                # hpsklearn.sgd_regression('mcpl_prediction.sgd_regression'),

                                # hpsklearn.lightgbm_regression('mcpl_prediction.lightgbm_regression'),
                                # hpsklearn.knn_regression
                                # hpsklearn.linear_discriminant_analysis('mcpl_prediction.linear_discriminant_analysis'),
                                # hpsklearn.quadratic_discriminant_analysis('mcpl_prediction.quadratic_discriminant_analysis'),
                                # hpsklearn.xgboost_regression('mcpl_prediction.xgboost_regression')
                                ])

        # We define the search procedure.
        # We will explore the regressor above and all data transforms available
        hyperopt_estimator = HyperoptEstimator(
                                regressor=regressors,  # any_regressor('reg'),
                                preprocessing=any_preprocessing('pre'),
                                # preprocessing=[hpsklearn.standard_scaler('standard_scaler')]
                                loss_fn=mean_squared_error,
                                algo=tpe.suggest, max_evals=HYPEROPT_MAX_EVALS,
                                trial_timeout=30)

        hyperopt_estimator.fit(X_train, y_train)

        # Performance
        y_test_predicted = hyperopt_estimator.predict(X_test)
        (rmse_test, r2_test, mae_test) = get_regression_metrics(y_test, y_test_predicted)
        # Track metrics in MLflow
        mlflow.log_metric("rmse_test", rmse_test)
        mlflow.log_metric("r2_test", r2_test)
        mlflow.log_metric("mae_test", mae_test)

        y_train_predicted = hyperopt_estimator.predict(X_train)
        (rmse_train, r2_train, mae_train) = get_regression_metrics(y_train,
                                                                   y_train_predicted)
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

        mlflow.set_tag("version", VERSION)
        # data_path = dvc.api.get_url(path=data_file_path, repo=PROJECT_PATH)
        # mlflow.set_tag("data path", data_path)
        mlflow.log_param("test_split_percent", MCPL_TEST_SPLIT)
        mlflow.log_param("test_split_seed", TEST_SPLIT_SEED)
