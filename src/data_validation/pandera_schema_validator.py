import logging

import pandera
import pandas as pd

from src.utils.files import get_json_from_file_path


logger = logging.getLogger(__name__)


class PanderaSchemaValidator():
    def __init__(self, schema: pandera.DataFrameSchema, data_path: str, data_name: str):
        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'
        self.data = self.get_data()
        self.schema = schema

    def validate_data(self):
        logger.info('======'*7)
        logger.info(f'Validating raw data. Name: {self.data_name}')
        # Load data to pandas DataFrame to validate it
        data_df = pd.DataFrame.from_dict(self.data)
        try:
            self.schema.validate(data_df, lazy=True)
            logger.info(f'Validated dataset schema succesfully.')

        except pandera.errors.SchemaErrors as err:
            msg = (f'\nDataset schema has not been validated: '
                   f'Exception trace and description:\n{err}')
            logger.error(msg)
            raise
        logger.info('======'*7)

    def get_data(self):
        data = get_json_from_file_path(self.full_data_path)
        return data
