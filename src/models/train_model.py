
import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler
import dvc.api
import mlflow
import mlflow.sklearn

from src.features.custom_transformations_sklearn import VariableRatioColsRowsAdder
from src.config_variables import (RAW_DATA_PATH, MCPL_TEST_SPLIT, TRAIN_MODEL_EXP_NAME,
                                  PROJECT_PATH, VERSION, ARTIFACT_LOCAL_PATH,
                                  MLFLOW_TRACKING_URI)
from src.utils.files import get_json_from_file_path
from src.utils.training import get_regression_metrics

logger = logging.getLogger(__name__)


def data_transformation_and_training(data_name: str, alpha: float,
                                     l1_ratio: float) -> str:
    """
    Tranform the dataset and train the linear model to predict the max character
    per line (MCPL). It loads the dataset, split it in training and test sets.
    Then, train the model (pipeline). Track the model in MLFlow as well as metrics
    computed in the test dataset to evaluate the model. Finally return the
    relative path of the model artifact tracked in MLflow.

    :param data_name: Name of the dataset
    :type data_name: str
    :param alpha: Constant that multiplies the penalty terms in the linear model
    :type alpha: float
    :param l1_ratio: The ElasticNet mixing parameter
    :type l1_ratio: float
    :return: Relative path of the artifact tracked in MLflow
    :rtype: str
    """

    logger.info('======'*7)
    logger.info(f'Training the model for MCPL prediction. Dataset name: {data_name}')

    # Load data to pandas DataFrame
    data_file_path = f'{RAW_DATA_PATH}/{data_name}.json'
    MCPL_dataset = get_json_from_file_path(data_file_path)
    MCPL_dataframe = pd.DataFrame.from_dict(MCPL_dataset)

    # The target variable is "max_char_per_line"
    X = MCPL_dataframe.drop("max_char_per_line", axis=1)
    y = MCPL_dataframe["max_char_per_line"]

    # Split the data into training and test sets.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=MCPL_TEST_SPLIT,
                                                        random_state=1)
    logger.info(f'X_train shape: {X_train.shape}')
    logger.info(f'X_test shape: {X_test.shape}')

    # Start a MLflow run
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(experiment_name=TRAIN_MODEL_EXP_NAME)
    with mlflow.start_run():

        # Define the pipeline (feature engineering, scaler, and model)
        pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                         ('scaler', StandardScaler()),
                         ('elasticnet', ElasticNet(alpha=alpha,
                                                   l1_ratio=l1_ratio,
                                                   random_state=42))])
        # Train the model
        fit_elasticnet = pipe.fit(X_train, y_train)

        # Predictions in the test set
        y_test_predicted = fit_elasticnet.predict(X_test)

        # Compute metrics in the test data
        (rmse, mae, r2) = get_regression_metrics(y_test, y_test_predicted)

        logger.info(f'Elasticnet model: alpha={alpha}, l1_ratio={l1_ratio} trained.')
        logger.info(f'Metrics: \nRMSE: {rmse} \nMAE: {mae} \nR2: {r2}')

        # Track information in MLflow (hyperparameters, metrics...)
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        data_path = dvc.api.get_url(path=data_file_path, repo=PROJECT_PATH)
        mlflow.set_tag("data path", data_path)
        mlflow.set_tag("version", VERSION)

        # Serialize the model in a format that MLflow knows how to deploy it
        mlflow.sklearn.log_model(pipe, ARTIFACT_LOCAL_PATH)
        # Get the relative path of the artifact (./models/123../artifacts)
        artifact_uri = mlflow.get_artifact_uri()
        return artifact_uri[7:]
