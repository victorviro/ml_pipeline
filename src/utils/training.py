"""
Utils used for training models
"""

import numpy as np
from numpy import ndarray
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score)


# Function to compute regression metrics
def get_regression_metrics(actual: ndarray, predictions: ndarray) -> tuple:
    """
    Compute metrics for a regression model evaluation.

    :param actual: True values of the target variable
    :type actual: ndarray
    :param predictions: Predicted values of the target variable
    :type predictions: ndarray
    :return: The metrics
    :rtype: tuple
    """
    rmse = np.sqrt(mean_squared_error(actual, predictions))
    mae = mean_absolute_error(actual, predictions)
    r2 = r2_score(actual, predictions)
    return rmse, mae, r2


def get_class_parameters(cls) -> list:
    """
    Get the parameters of a class (usually a sklearn class method).
    It first get al attributes of the class and filter the parameters

    :return: The name of the parameters of the class
    :rtype: list
    """
    parameters = []
    for attribute in cls.__dict__.keys():
        # Check if the attribute is a parameter
        is_parameter = attribute[:1] != '_' and attribute[-1:] != '_'
        if is_parameter:
            parameters.append(attribute)
    return parameters
