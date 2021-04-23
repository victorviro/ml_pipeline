"""
Define custom transformations to use in Sklearn pipelines
"""

from sklearn.base import BaseEstimator, TransformerMixin
from pandas import DataFrame
from numpy import ndarray, hstack


class VariableRatioColsRowsAdder(BaseEstimator, TransformerMixin):

    """
    Add a new variable: cols number divided by rows number
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    # Define the transformation
    def transform(self, X):
        X_new = X.copy()
        # Add a new variable
        if isinstance(X_new, DataFrame):
            X_new["ratio_cols_rows"] = X.cols_number/X.rows_number
        if isinstance(X_new, ndarray):
            ratio_cols_rows = X[:, 2:3]/X[:, 1:2]
            X_new = hstack((X_new, ratio_cols_rows))
        return X_new
