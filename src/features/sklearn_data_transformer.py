import logging

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.utils.files import get_json_from_file_path, save_json_file
from src.features.custom_transformations_sklearn import VariableRatioColsRowsAdder


logger = logging.getLogger(__name__)


class SklearnDataTransformer:
    def __init__(self,  data_path: str, data_name: str, data_output_path: str):
        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'
        self.data = self.get_data()
        self.full_data_output_path = f'{data_output_path}/{data_name}_processed.json'

    def transform_data(self):
        logger.info('======'*7)
        logger.info(f'Transforming raw data. Name: {self.data_name}')
        # Load data to pandas DataFrame
        data_df = pd.DataFrame.from_dict(self.data)
        data_columns = data_df.columns.to_list()
        # Define the pipeline (feature engineering, scaler, and model)
        pipe = Pipeline([('add_ratio_cols_rows', VariableRatioColsRowsAdder()),
                         ('scaler', StandardScaler())])
        data_columns.append('ratio_cols_rows')
        data_tranformed_array = pipe.fit_transform(data_df)
        data_transformed_df = pd.DataFrame(data_tranformed_array,
                                           columns=data_columns)
        data_transformed = data_transformed_df.to_dict(orient='list')
        # Store the data transformed
        self.save_data(data=data_transformed, full_data_path=self.full_data_output_path)

    def get_data(self):
        data = get_json_from_file_path(self.full_data_path)
        return data

    def save_data(self, data: dict, full_data_path: str):
        save_json_file(file_path=full_data_path, content=data)
        logger.info(f'Stored data transformed in {full_data_path}')
        logger.info('======'*7)
