import logging

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.shared.files_helper import (get_json_from_file_path, save_json_file,
                                     save_pickle_file, load_pickle_file)
from .custom_transformation_sklearn import VariableRatioColsRowsAdder

logger = logging.getLogger(__name__)


class SklearnDataTransformer:

    def transform_data(self, raw_data: dict, transformer_pipeline: Pipeline) -> dict:

        # Load data to pandas DataFrame and transform it
        try:
            data_df = pd.DataFrame.from_dict(raw_data)
            data_columns = data_df.columns.to_list()
            data_columns.append('ratio_cols_rows')
            data_tranformed_array = transformer_pipeline.transform(data_df)
            data_transformed_df = pd.DataFrame(data_tranformed_array,
                                               columns=data_columns)
            data_transformed = data_transformed_df.to_dict(orient='list')
        except Exception as err:
            msg = f'Error when transforming data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        return data_transformed


class SklearnTrainDataTransformer(SklearnDataTransformer):
    def __init__(self,  data_path: str, data_name: str, data_output_path: str,
                 model_path: str, pipe_name: str):
        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'
        self.full_data_output_path = f'{data_output_path}/{data_name}_processed.json'
        self.full_pipe_output_path = f'{model_path}/{pipe_name}.pkl'

    def get_data(self) -> dict:

        try:
            raw_data = get_json_from_file_path(self.full_data_path)
            logger.info(f'Loaded data succesfully.')
        except Exception as err:
            msg = f'Error loading data. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        return raw_data

    def save_data(self, data_transformed: dict):
        # Store the data transformed
        try:
            save_json_file(file_path=self.full_data_output_path, content=data_transformed)
            msg = ('Training dataset transformed stored succesfully in path: '
                   f'{self.full_data_output_path}')
            logger.info(msg)
        except Exception as err:
            msg = f'Error storing the train dataset transformed. Traceback error: {err}'
            logger.error(msg)
            raise Exception(msg)

    def save_transformer_pipeline(self, transformer_pipeline: Pipeline):
        # Store the data transformed
        try:
            save_pickle_file(file_path=self.full_pipe_output_path,
                             file=transformer_pipeline)
            msg = ('Transformer pipeline saved succesfully in path: '
                   f'{self.full_pipe_output_path}')
            logger.info(msg)
        except Exception as err:
            msg = f'Error storing the transformer pipeline. Traceback error: {err}'
            logger.error(msg)
            raise Exception(msg)

    def fit_transfomer_pipeline(self, raw_data: dict) -> Pipeline:
        # Load data to pandas DataFrame and get transfomer pipeline
        try:
            data_df = pd.DataFrame.from_dict(raw_data)
            # Define the pipeline (feature engineering, scaler, and model)
            pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                             ('scaler', StandardScaler())])
            transformer_pipeline = pipe.fit(data_df)

        except Exception as err:
            msg = f'Error fitting transfomer pipeline. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        return transformer_pipeline
