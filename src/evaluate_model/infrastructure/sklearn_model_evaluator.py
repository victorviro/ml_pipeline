import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.shared.training_helper import get_regression_metrics
from src.evaluate_model.domain.model_evaluator import IModelEvaluator


logger = logging.getLogger(__name__)


class SklearnModelEvaluator(IModelEvaluator):
    """
    A class which implements the interface IModelEvaluator to evaluate the model.
    It evaluate the model using different metrics and track the results.

    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    """

    def __init__(self, size_test_split: float, test_split_seed: int):
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def evaluate_model(self, data: dict, model: Pipeline) -> dict:
        """
        Evaluate the model using different metrics and track the results.

        :param data: The dataset used to validate the model (before splitting it)
        :type data: dict
        :param model: The sklearn model fitted (preprocessing + model)
        :type model: Pipeline
        :return: Information (metrics) to track
        :rtype: dict
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

        # Make predictions and compute metrics on the test and training sets
        try:
            y_test_predicted = model.predict(X_test)
            (rmse_test, mae_test, r2_test) = get_regression_metrics(y_test,
                                                                    y_test_predicted)
            y_train_predicted = model.predict(X_train)
            (rmse_train, mae_train, r2_train) = get_regression_metrics(
                y_train, y_train_predicted
            )

            logger.info(f'Metrics train set: \nRMSE: {rmse_train} \nMAE: {mae_train}'
                        f' \nR2: {r2_train}')
            logger.info(f'Metrics test set: \nRMSE: {rmse_test} \nMAE: {mae_test}'
                        f' \nR2: {r2_test}')

        except Exception as err:
            msg = ('Error making predictions or getting metrics on test and training sets'
                   f'. Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)

        metrics_to_track = {
            "rmse_train": rmse_train,
            "r2_train": r2_train,
            "mae_train": mae_train,
            "rmse_test": rmse_test,
            "r2_test": r2_test,
            "mae_test": mae_test
        }
        information_to_track = {
            "metrics": metrics_to_track,
        }
        return information_to_track
