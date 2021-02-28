import logging

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.utils.files import get_json_from_file_path, save_json_file
from .custom_transformation_sklearn import VariableRatioColsRowsAdder

logger = logging.getLogger(__name__)


class SklearnDataTransformer:
    def __init__(self,  data_path: str, data_name: str, data_output_path: str):
        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'
        self.full_data_output_path = f'{data_output_path}/{data_name}_processed.json'

    def transform_data(self):

        logger.info(f'Transforming raw data. Name: {self.data_name}')
        # Get data
        try:
            raw_data = get_json_from_file_path(self.full_data_path)
            logger.info(f'Loaded data succesfully.')
        except Exception as err:
            msg = f'Error loading data. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Load data to pandas DataFrame and transform it
        try:
            data_df = pd.DataFrame.from_dict(raw_data)
            data_columns = data_df.columns.to_list()
            # Define the pipeline (feature engineering, scaler, and model)
            pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                             ('scaler', StandardScaler())])
            data_columns.append('ratio_cols_rows')
            data_tranformed_array = pipe.fit_transform(data_df)
            data_transformed_df = pd.DataFrame(data_tranformed_array,
                                               columns=data_columns)
            data_transformed = data_transformed_df.to_dict(orient='list')
        except Exception as err:
            msg = f'Error when tranforming data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Store the data transformed
        try:
            save_json_file(file_path=self.full_data_output_path, content=data_transformed)
            msg = ('Dataset transformed stored succesfully in path: '
                   f'{self.full_data_output_path}')
            logger.info(msg)
        except Exception as err:
            msg = f'Error storing the dataset transformed. Traceback error: {err}'
            logger.error(msg)
            raise Exception(msg)
