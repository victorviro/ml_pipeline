import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from .custom_transformation_sklearn import VariableRatioColsRowsAdder
from src.transform_data.domain.transformation_fitter import ITransformationFitter


logger = logging.getLogger(__name__)


class SklearnTransformationFitter(ITransformationFitter):
    """
    A class which implements the interface ITransformationFitter to  fit a transformer.
    It fits a Scikit-learn pipeline to transform data.
    """

    def fit_transformer(self, data: dict, size_test_split: float,
                        test_split_seed: int) -> Pipeline:
        """
        Fit a Scikit-learn pipeline to transform data.

        :param data: The dataset used to fit the transformer (after splitting it)
        :type data: dict
        :param size_test_split: Percentage of test dataset when splitting the dataset
        :type size_test_split: float
        :param test_split_seed: Seed used when splitting the dataset
        :type test_split_seed: int
        :return: The transformer pipeline fitted
        :rtype: Pipeline
        """

        try:
            # Load data to pandas DataFrame
            data_df = DataFrame.from_dict(data)
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
            # Split the dataset in train and test sets
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=size_test_split, random_state=test_split_seed
            )
            # Define and fit the pipeline (feature engineering and scaler)
            pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                             ('standard_scaler', StandardScaler())])
            transformer_pipeline = pipe.fit(X_train)
            return transformer_pipeline

        except Exception as err:
            msg = f'Error fitting transfomer pipeline. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
