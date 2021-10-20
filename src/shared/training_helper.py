"""
Utils used for training models
"""
import logging
from typing import Tuple

import numpy as np
from numpy import ndarray
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logger = logging.getLogger(__name__)


def get_regression_metrics(
    actual: ndarray, predictions: ndarray
) -> Tuple[float, float, float]:
    """
    Compute metrics for a regression model evaluation.

    :param actual: True values of the target variable
    :type actual: ndarray
    :param predictions: Predicted values of the target variable
    :type predictions: ndarray
    :return: The metrics
    :rtype: tuple
    """
    try:
        rmse = np.sqrt(mean_squared_error(actual, predictions))
        mae = mean_absolute_error(actual, predictions)
        r_square = r2_score(actual, predictions)
    except Exception as err:
        msg = "Error trying to compute regresion metrics."
        logger.error(msg)
        raise Exception(msg) from err
    return rmse, mae, r_square


def get_class_parameters(cls) -> list:
    """
    Get the parameters of a class (usually a sklearn class method).
    It first get al attributes of the class and filter the parameters

    :return: The name of the parameters of the class
    :rtype: list
    """
    parameters = []
    try:
        for attribute in cls.__dict__.keys():
            # Check if the attribute is a parameter
            is_parameter = attribute[:1] != "_" and attribute[-1:] != "_"
            if is_parameter:
                parameters.append(attribute)
    except Exception as err:
        msg = f"Error trying to get parameters of class: {cls}."
        logger.error(msg)
        raise Exception(msg) from err
    return parameters
