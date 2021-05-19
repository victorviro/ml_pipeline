import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.shared.training_helper import get_regression_metrics
from src.validate_model.domain.model_validator import IModelValidator


logger = logging.getLogger(__name__)


class SklearnModelValidator(IModelValidator):
    """
    A class which implements the interface IModelValidator to validate the model.
    It validates the model if the root mean squared error (rmse) in the test set
    is smaller than a value given. If the model is not validated, it raises an
    exception.

    :param rmse_threshold: Threshold to validate the model using the rmse
    :type rmse_threshold: float
    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    """
    def __init__(self, rmse_threshold: float, size_test_split: float,
                 test_split_seed: int):
        self.rmse_threshold = rmse_threshold
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def validate_model(self, data: dict, model: Pipeline):
        """
        Validate the model if the root mean squared error (rmse) in the test set
        is smaller than a value given. If the model is not validated, it raises an
        exception.

        :param data: The dataset used to validate the model (before splitting it)
        :type data: dict
        :param model: The sklearn model fitted (preprocessing + model)
        :type model: Pipeline
        """

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
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
            logger.info(f'Dataset splitted succesfully.')
        except Exception as err:
            msg = f'Error getting target variable or splitting data. Error: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Make predictions and compute metrics on the test set
        try:
            y_test_predicted = model.predict(X_test)
            (rmse, mae, r2) = get_regression_metrics(y_test, y_test_predicted)

        except Exception as err:
            msg = ('Error making predictions or getting metrics on test set'
                   f'. Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)

        logger.info(f'Metrics: \nRMSE: {rmse} \nMAE: {mae} \nR2: {r2}')

        if rmse > self.rmse_threshold:
            msg = ('Square root of mean squared error bigger that the thresold fixed:'
                   f' {rmse} > thresold fixed = {self.rmse_threshold}')
            raise Exception(f'Model was not validated succesfully in test set: {msg}')
        else:
            msg = ('Square root of mean squared error smaller that the thresold fixed:'
                   f' {rmse} < thresold fixed = {self.rmse_threshold}')
            logger.info(f'Model validated succesfully in test set: {msg}')
