import logging

import pandera
import pandas as pd

from src.utils.files import get_json_from_file_path


# Define the schema of the dataset
MCPL_SCHEMA = pandera.DataFrameSchema({
    "max_char_per_line": pandera.Column(int,
                                        checks=pandera.Check.less_than_or_equal_to(100)),
    "font_size": pandera.Column(int, checks=pandera.Check.less_than(1000)),
    "rows_number": pandera.Column(int),
    "cols_number": pandera.Column(int),
    "char_number_text": pandera.Column(int)
})


logger = logging.getLogger(__name__)


class PanderaSchemaValidator():
    def __init__(self, data_path: str, data_name: str):
        self.data_path = data_path
        self.data_name = data_name
        self.full_data_path = f'{data_path}/{data_name}.json'

    def validate_data(self):

        logger.info(f'Validating raw data. Name: {self.data_name}')

        # Get data
        try:
            raw_data = get_json_from_file_path(self.full_data_path)
            logger.info(f'Loaded data succesfully.')
        except Exception as err:
            msg = f'Error loading data. Error traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        # Load data to pandas DataFrame to validate it
        data_df = pd.DataFrame.from_dict(raw_data)
        try:
            MCPL_SCHEMA.validate(data_df, lazy=True)
            logger.info('Validated dataset schema succesfully.')

        except Exception as err:
            if isinstance(err, pandera.errors.SchemaErrors):
                msg = ('Dataset schema has not been validated: '
                       f'Exception trace and description:\n{err}')
                logger.error(msg)
                raise Exception(msg)
            msg = f'Error when validating data schema. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
