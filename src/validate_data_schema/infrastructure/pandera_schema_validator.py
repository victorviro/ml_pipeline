import logging

import pandas as pd
import pandera
from pandera.errors import SchemaErrors
from pandera.schemas import DataFrameSchema

from src.validate_data_schema.domain.data_validator import IDataValidator

logger = logging.getLogger(__name__)


class PanderaSchemaValidator(IDataValidator):
    """
    A class which implements the interface IDataValidator to validate the dataset.
    It validates the schema of the dataset in pandas DataFrame format using Pandera.
    """

    def validate_data(self, dataset: dict, dataset_schema_info: list):
        """
        Validate the schema of the dataset in pandas DataFrame format using Pandera.

        :param dataset: The dataset to be validated
        :type dataset: dict
        :param dataset_schema_info: Information of the valid schema of the dataset
        :type dataset_schema_info: list
        """

        logger.info("Validating raw dataset...")

        # Load dataset in pandas DataFrame format
        try:
            dataset_df = pd.DataFrame.from_dict(dataset)
            logger.info("Converted dataset to pandas DataFrame succesfully.")

        except ValueError as err:
            msg = "Value error converting JSON dataset to pandas DataFrame."
            logger.error(msg)
            raise ValueError(msg) from err

        except Exception as err:
            msg = "Unknown error converting dataset to pandas DataFrame."
            logger.error(msg)
            raise Exception(msg) from err

        # Get the valid schema of the dataset (pandera object)
        pandera_dataset_schema = self._get_pandera_dataset_schema(
            dataset_schema_info=dataset_schema_info
        )
        # Validate the schema of the dataset
        try:
            pandera_dataset_schema.validate(dataset_df, lazy=True)
            logger.info("Dataset schema validated succesfully.")

        except SchemaErrors as err:
            msg = (
                "Dataset schema has been violated. Schema errors found:\n"
                f"{err.schema_errors}"
            )
            logger.error(msg)
            raise err

        except Exception as err:
            msg = "Unknown error when validating dataset schema."
            logger.error(msg)
            raise Exception(msg) from err

    @staticmethod
    def _get_pandera_dataset_schema(dataset_schema_info: list) -> DataFrameSchema:
        """
        Get the valid schema of the dataset (pandera object) to validate the dataset.

        :param dataset_schema_info: Information of the schema of the dataset
        :type dataset_schema_info: list
        :return: The valid schema of the dataset (pandera object)
        :rtype: DataFrameSchema
        """
        pandera_dataset_schema_dict = {}
        for variable_info in dataset_schema_info:
            try:
                variable_name = variable_info["name"]
                # Checks to verify validity of the column
                range_condition = (
                    variable_info["greater"] is not None
                    and variable_info["less"] is not None
                )
                if range_condition:
                    checks = pandera.Check.in_range(
                        min_value=variable_info["greater"],
                        max_value=variable_info["less"],
                    )
                elif variable_info["greater"] is not None:
                    checks = pandera.Check.greater_than_or_equal_to(
                        min_value=variable_info["greater"]
                    )
                elif variable_info["less"] is not None:
                    checks = pandera.Check.less_than_or_equal_to(
                        max_value=variable_info["less"]
                    )
                # Create column validator of pandera for the variable
                pandera_column = pandera.Column(
                    pandas_dtype=variable_info["type"],
                    nullable=variable_info["nullable"],
                    name=variable_name,
                    checks=checks,
                )
                # Update dict
                pandera_dataset_schema_dict.update({variable_name: pandera_column})
            except TypeError as err:
                msg = (
                    "TypeError creating pandera dataset schema of the variable: "
                    f" {variable_name}."
                )
                raise TypeError(msg) from err
            except KeyError as err:
                msg = (
                    "Error accessing a value of a dict with an invalid key. Key not :"
                    f"found: {err}. Dict: {variable_info}"
                )
                raise KeyError(msg) from err

        pandera_dataset_schema = pandera.DataFrameSchema(pandera_dataset_schema_dict)
        return pandera_dataset_schema
