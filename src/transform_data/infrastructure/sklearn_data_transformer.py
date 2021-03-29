import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from src.shared.files_helper import (get_json_from_file_path,
                                     save_pickle_file, load_pickle_file)
from .custom_transformation_sklearn import VariableRatioColsRowsAdder


logger = logging.getLogger(__name__)


class SklearnDataTransformer:
    """
    A class which implements the interface IDataTransformer to transform the data.
    It transform the data using a Scikit-learn pipeline fitted previously.

    :param transformer_pipe_path: Path where the transformer pipeline is stored
    :type transformer_pipe_path: str
    :param pipe_name: Name of the transformer pipeline file stored
    :type pipe_name: str
    """

    def __init__(self, transformer_pipe_path: str, pipe_name: str):
        self.full_pipe_path = f'{transformer_pipe_path}/{pipe_name}.pkl'

    def transform_data(self, raw_data: dict) -> dict:

        # Load data to pandas DataFrame and transform it
        try:
            data_df = DataFrame(raw_data)
            data_columns = data_df.columns.to_list()
            data_columns.append('ratio_cols_rows')
            self.load_transformer_pipeline()
            data_tranformed_array = self.transformer_pipeline.transform(data_df)
            data_transformed_df = DataFrame(data_tranformed_array,
                                            columns=data_columns)
            data_transformed = data_transformed_df.to_dict(orient='list')
        except Exception as err:
            msg = f'Error when transforming data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        return data_transformed

    def load_transformer_pipeline(self):
        try:
            transformer_pipeline = load_pickle_file(self.full_pipe_path)
            self.transformer_pipeline = transformer_pipeline
        except Exception as err:
            msg = f'Error loading the transformer pipeline. Traceback error: {err}'
            logger.error(msg)
            raise Exception(msg)


class SklearnFitDataTransformer:
    """
    A class which fits and store a Scikit-learn pipeline to transform data.

    :param data_path: Path where the data is stored
    :type data_path: str
    :param data_name: Name of the dataset
    :type data_name: str
    :param transformer_pipe_path: Path where the transformer pipeline will be stored
    :type transformer_pipe_path: str
    :param pipe_name: Name of the transformer pipeline file to be stored
    :type pipe_name: str
    :param size_test_split: Percentage of test dataset when splitting the dataset
    :type size_test_split: float
    :param test_split_seed: Seed used when splitting the dataset
    :type test_split_seed: int
    """
    def __init__(self,  data_path: str, data_name: str,
                 transformer_pipe_path: str, pipe_name: str, size_test_split: float,
                 test_split_seed: int):

        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'
        self.full_pipe_output_path = f'{transformer_pipe_path}/{pipe_name}.pkl'
        self.size_test_split = size_test_split
        self.test_split_seed = test_split_seed

    def fit_transfomer_pipeline(self):
        # Load data to pandas DataFrame, split it in train and test sets, and fit
        # transfomer pipeline
        try:
            raw_data = get_json_from_file_path(self.full_data_path)
            data_df = DataFrame.from_dict(raw_data)
            X = data_df.drop("max_char_per_line", axis=1)
            y = data_df["max_char_per_line"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.size_test_split, random_state=self.test_split_seed
            )
            # Define and fit the pipeline (feature engineering and scaler)
            pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                             ('standard_scaler', StandardScaler())])
            transformer_pipeline = pipe.fit(X_train)
            self.transformer_pipeline = transformer_pipeline

        except Exception as err:
            msg = f'Error fitting transfomer pipeline. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

    def save_transformer_pipeline(self):
        # Store the data transformed
        try:
            save_pickle_file(file_path=self.full_pipe_output_path,
                             file=self.transformer_pipeline)
            msg = ('Transformer pipeline saved succesfully in path: '
                   f'{self.full_pipe_output_path}')
            logger.info(msg)
        except Exception as err:
            msg = f'Error storing the transformer pipeline. Traceback error: {err}'
            logger.error(msg)
            raise Exception(msg)
