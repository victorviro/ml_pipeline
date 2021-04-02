import logging

import pandera
import pandas as pd

from src.validate_data_schema.domain.data_validator import IDataValidator


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


class PanderaSchemaValidator(IDataValidator):
    """
    A class which implements the interface IDataValidator to validate the dataset.
    It validates the schema of the dataset in pandas DataFrame format using Pandera.

    :param dataset_schema: The valid schema to validate the dataset
    :type dataset_schema: pandera.DataFrameSchema
    """

    def __init__(self, dataset_schema: pandera.DataFrameSchema):
        self.dataset_schema = dataset_schema

    def validate_data(self, data: dict):
        """
        Validate the schema of data in pandas DataFrame format using Pandera.

        :param data: The dataset to be validated
        :type data: dict
        """

        logger.info(f'Validating raw data')

        # Load data in pandas DataFrame format
        try:
            data_df = pd.DataFrame.from_dict(data)
            logger.info(f'Converted data to pandas DataFrame succesfully.')

        except Exception as err:
            msg = ('Error converting data to pandas DataFrame. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise Exception(msg)

        # Validate the schema of the dataset
        try:
            self.dataset_schema.validate(data_df, lazy=True)
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
