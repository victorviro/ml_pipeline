import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from src.transform_data.domain.transformation_fitter import ITransformationFitter
from src.shared.interfaces.data_file_saver import IDataFileSaver
from src.shared.interfaces.data_tracker import IDataTracker

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
    def __init__(self, size_test_split: float, test_split_seed: int,
                 transformer_file_path: str, model_name: str):
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed
        self.transformer_file_path = transformer_file_path
        self.model_name = model_name

    def fit_transformer(self, data: dict, data_file_saver: IDataFileSaver,
                        data_tracker: IDataTracker) -> Pipeline:
        """
        Fit a Scikit-learn pipeline to transform data.

        :param data: The dataset used to fit the transformer (after splitting it)
        :type data: dict
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
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
            # Define and fit the pipeline (feature engineering and scaler)
            pipe = Pipeline([('standard_scaler', StandardScaler())])
            transformer_pipeline = pipe.fit(X_train)
            logger.info('Transformer pipeline fitted succesfully.')

        except Exception as err:
            msg = f'Error fitting transfomer pipeline. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        try:
            # Save the transformer pipeline
            data_file_saver.save_data(
                file_path=self.transformer_file_path,
                file=transformer_pipeline
            )
        except Exception as err:
            raise Exception('Error saving the sklearn transformer pipeline in path: '
                            f'{self.transformer_file_path}. Traceback: {err}')

        try:
            # Track the transformer pipeline as an artifact into the MLflow experiment
            artifact_path = data_tracker.track_sklearn_transfomer_pipeline(
                file_path=self.transformer_file_path,
                model_name=self.model_name,
                transformer_pipe=transformer_pipeline
            )
            return artifact_path
        except Exception as err:
            raise Exception('Error tracking the sklearn transformer pipeline. '
                            f'Traceback: {err}')
