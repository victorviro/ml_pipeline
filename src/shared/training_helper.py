"""
Utils used for training models
"""
import logging
from typing import Tuple

import numpy as np
import numpy.typing as npt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

logger = logging.getLogger(__name__)


def get_regression_metrics(
    actual: npt.NDArray[np.float32], predictions: npt.NDArray[np.float32]
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
