
import logging

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

from src.config_variables import RAW_DATA_PATH, MCPL_TEST_SPLIT, RMSE_THRESOLD
from src.utils.files import get_json_from_file_path
from src.utils.training import get_regression_metrics

logger = logging.getLogger(__name__)


def validate_model(data_name: str, model_path: str):

    logger.info('======'*7)
    logger.info(f'Validating the model for MCPL prediction. Dataset name: {data_name}')

    # Load data to pandas DataFrame
    data_file_path = f'{RAW_DATA_PATH}/{data_name}.json'
    MCPL_dataset = get_json_from_file_path(data_file_path)
    MCPL_dataframe = pd.DataFrame.from_dict(MCPL_dataset)

    # The predicted column is "max_char_per_line"
    X = MCPL_dataframe.drop("max_char_per_line", axis=1)
    y = MCPL_dataframe["max_char_per_line"]

    # Split the data into training and test sets. (0.75, 0.25) split.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=MCPL_TEST_SPLIT,
                                                        random_state=1)
    logger.info(f'X_train shape: {X_train.shape}')
    logger.info(f'X_test shape: {X_test.shape}')

    # Load the trained model back from file
    with open(model_path, 'rb') as file:
        pipe = pickle.load(file)

    # Get performance in validation data
    # Predictions in the test set
    y_test_predicted = pipe.predict(X_test)

    # Compute metrics in the test data
    (rmse, mae, r2) = get_regression_metrics(y_test, y_test_predicted)

    logger.info(f'Metrics: \nRMSE: {rmse} \nMAE: {mae} \nR2: {r2}')

    if rmse > RMSE_THRESOLD:
        msg = ('Square root of mean squared error bigger that the thresold fixed:'
               f' {rmse} > thresold fixed = {RMSE_THRESOLD}')
        raise Exception(msg)
    else:
        msg = ('Square root of mean squared error smaller that the thresold fixed:'
               f' {rmse} < thresold fixed = {RMSE_THRESOLD}')
        logger.info(f'Model validated in validation dataset: {msg}')
    logger.info('======'*7)
