import logging

from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.shared.constants import TARGET_VARIABLE_NAME
from src.transform_data.domain.transformation_fitter import ITransformationFitter

logger = logging.getLogger(__name__)


class SklearnTransformationFitter(ITransformationFitter):
    def __init__(self, size_test_split: float, test_split_seed: int):
        """
        :param size_test_split: Percentage of test dataset when splitting the dataset
        :type size_test_split: float
        :param test_split_seed: Seed used when splitting the dataset
        :type test_split_seed: int
        """
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def fit_transformer(self, dataset: dict) -> Pipeline:

        # Load the dataset to pandas DataFrame
        dataset_df = DataFrame.from_dict(dataset)
        features = dataset_df.drop(TARGET_VARIABLE_NAME, axis=1)
        target = dataset_df[TARGET_VARIABLE_NAME]
        # Split the dataset in train and test sets
        try:
            x_train, _, _, _ = train_test_split(
                features,
                target,
                test_size=self.size_test_split,
                random_state=self.test_split_seed,
            )
        except ValueError as err:
            msg = "ValueError splitting the dataset into training and test sets."
            raise ValueError(msg) from err
        # Define and fit the pipeline (standard scaler)
        try:
            pipeline = Pipeline([("standard_scaler", StandardScaler())])
            transformer_pipeline = pipeline.fit(x_train)
            logger.info("Transformer pipeline fitted succesfully.")
            return transformer_pipeline
        except Exception as err:
            msg = "Error fitting transfomer pipeline."
            logger.error(msg)
            raise Exception(msg) from err
