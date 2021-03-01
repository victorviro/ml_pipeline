import logging

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.files import get_json_from_file_path, load_pickle_file
from src.utils.training import get_regression_metrics


logger = logging.getLogger(__name__)


class SklearnModelValidator():
    def __init__(self, transformed_data_path: str, data_name: str, model_path: str,
                 model_name: str, rmse_threshold: float, size_test_split: float,
                 test_split_seed: int):
        self.transformed_data_path = transformed_data_path
        self.data_name = data_name
        self.full_transformed_data_path = (f'{transformed_data_path}/{data_name}'
                                           '_processed.json')
        self.model_path = model_path
        self.model_name = model_name
        self.full_model_path = f'{model_path}/{model_name}.pkl'
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
            model = load_pickle_file(self.full_model_path)
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
            raise Exception(msg)
        else:
            msg = ('Square root of mean squared error smaller that the thresold fixed:'
                   f' {rmse} < thresold fixed = {self.rmse_threshold}')
            logger.info(f'Model validated succesfully in test set: {msg}')
