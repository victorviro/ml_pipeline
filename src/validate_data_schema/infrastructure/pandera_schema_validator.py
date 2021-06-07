import logging

import pandera
import pandas as pd
from pandera.errors import SchemaErrors

from src.validate_data_schema.domain.data_validator import IDataValidator


# Define the schema of the dataset TODO
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

        logger.info(f'Validating raw dataset...')

        # Load dataset in pandas DataFrame format
        try:
            data_df = pd.DataFrame.from_dict(data)
            logger.info(f'Converted dataset to pandas DataFrame succesfully.')

        except ValueError as err:
            msg = ('Value error converting JSON dataset to pandas DataFrame. '
                   f'Error traceback: {err}')
            logger.error(msg)
            raise ValueError(msg)

        except Exception as err:
            msg = ('Unknown error converting dataset to pandas DataFrame. '
                   f'Error traceback: {err.__class__.__name__}: {err}')
            logger.error(msg)
            raise Exception(msg)

        # Validate the schema of the dataset
        try:
            self.dataset_schema.validate(data_df, lazy=True)
            logger.info('Dataset schema validated succesfully.')

        except SchemaErrors as err:
            msg = ('Dataset schema has been violated. Schema errors found:\n'
                   f'{err.schema_errors}')
            logger.error(msg)
            raise err

        except Exception as err:
            msg = ('Unknown error when validating dataset schema. Traceback: '
                   f'{err.__class__.__name__}: {err}')
            logger.error(msg)
            raise Exception(msg)
