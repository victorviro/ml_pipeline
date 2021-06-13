import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.shared.training_helper import get_regression_metrics
from src.evaluate_model.domain.model_evaluator import IModelEvaluator
from src.shared.constants import TARGET_VARIABLE_NAME


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

    def evaluate_model(self, dataset: dict, model: Pipeline) -> dict:
        """
        Evaluate the model using different metrics and track the results.

        :param dataset: The dataset used to validate the model (before splitting it)
        :type dataset: dict
        :param model: The sklearn model fitted (preprocessing + model)
        :type model: Pipeline
        :return: Information (metrics) to track
        :rtype: dict
        """

        # Load the dataset to pandas DataFrame
        dataset_df = DataFrame.from_dict(dataset)
        X = dataset_df.drop(TARGET_VARIABLE_NAME, axis=1)
        y = dataset_df[TARGET_VARIABLE_NAME]

        # Split the dataset in training and test sets.
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
            logger.info('Dataset split succesfully.')
        except ValueError as err:
            msg = ('ValueError splitting the dataset in training and test sets. Error '
                   f'description: {err}.')
            raise ValueError(msg)

        # Make predictions and compute metrics on the test and training sets
        try:
            y_test_predicted = model.predict(X_test)
            (rmse_test, mae_test, r2_test) = get_regression_metrics(y_test,
                                                                    y_test_predicted)
            y_train_predicted = model.predict(X_train)
            (rmse_train, mae_train, r2_train) = get_regression_metrics(y_train,
                                                                       y_train_predicted)

        except Exception as err:
            msg = ('Error making predictions or getting metrics on test and training sets'
                   f'. Error description: {err.__class__.__name__}: {err}.')
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
