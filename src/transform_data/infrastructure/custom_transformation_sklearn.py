"""
Define custom transformations to use in Sklearn pipelines
"""

from sklearn.base import BaseEstimator, TransformerMixin


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
        X_new["ratio_cols_rows"] = X.cols_number/X.rows_number
        return X_new
