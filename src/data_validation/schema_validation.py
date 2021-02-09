
import logging

import pandas as pd
import pandera

from src.data_validation.schemas.MCPL import MCPL_schema
from src.config_variables import RAW_DATA_PATH
from src.utils.files import get_json_from_file_path


logger = logging.getLogger(__name__)


# Define the schema of the dataset
MCPL_schema = pandera.DataFrameSchema({
    "max_char_per_line": pandera.Column(int,
                                        checks=pandera.Check.less_than_or_equal_to(100)),
    "font_size": pandera.Column(int, checks=pandera.Check.less_than(1000)),
    "rows_number": pandera.Column(int),
    "cols_number": pandera.Column(int),
    "char_number_text": pandera.Column(int)
})


def validate_data_schema(data_name):
    """
    Validate schema of raw data. Use pandera. Info:
    https://pandera.readthedocs.io/en/stable/lazy_validation.html

    :param data_name: Name of the dataset to be stored
    :type data_name: str
    """

    logger.info('======'*7)
    logger.info(f'Validating raw data. Name: {data_name}')

    # Load data to pandas DataFrame to validate it
    data_file_path = f'{RAW_DATA_PATH}/{data_name}.json'
    logger.info(f'Path of the dataset to load is {data_file_path}')
    MCPL_dataset = get_json_from_file_path(data_file_path)
    MCPL_df = pd.DataFrame.from_dict(MCPL_dataset)

    # Validate the dataset
    try:
        MCPL_schema.validate(MCPL_df, lazy=True)
        logger.info(f'Validated dataset schema succesfully.')

    except pandera.errors.SchemaErrors as err:
        msg = (f'\nDataset schema has not been validated: '
               f'Exception trace and description:\n{err}')
        logger.error(msg)
        raise
    logger.info('======'*7)
