import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from src.transform_data.domain.transformation_fitter import ITransformationFitter
from src.shared.constants import TARGET_VARIABLE_NAME


logger = logging.getLogger(__name__)


class SklearnTransformationFitter(ITransformationFitter):
    """
    A class which implements the interface ITransformationFitter to fit a transformer.
    It fits a Scikit-learn pipeline to transform data.

    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    """
    def __init__(self, size_test_split: float, test_split_seed: int):
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def fit_transformer(self, dataset: dict) -> Pipeline:
        """
        Fit a Scikit-learn pipeline to transform data.

        :param dataset: The dataset used to fit the transformer (after splitting it)
        :type dataset: dict
        :return: The transformer pipeline fitted
        :rtype: Pipeline
        """

        # Load the dataset to pandas DataFrame
        dataset_df = DataFrame.from_dict(dataset)
        X = dataset_df.drop(TARGET_VARIABLE_NAME, axis=1)
        y = dataset_df[TARGET_VARIABLE_NAME]
        # Split the dataset in train and test sets
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
        except ValueError as err:
            msg = ('ValueError splitting the dataset into training and test sets. Error '
                   f'description: {err}')
            raise ValueError(msg)
        # Define and fit the pipeline (standard scaler)
        try:
            pipeline = Pipeline([('standard_scaler', StandardScaler())])
            transformer_pipeline = pipeline.fit(X_train)
            logger.info('Transformer pipeline fitted succesfully.')
            return transformer_pipeline
        except Exception as err:
            msg = ('Error fitting transfomer pipeline. Error description: '
                   f'{err.__class__.__name__}: {err}')
            logger.error(msg)
            raise Exception(msg)
