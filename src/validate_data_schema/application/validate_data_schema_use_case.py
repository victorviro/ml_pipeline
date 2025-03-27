from __future__ import annotations

import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.validate_data_schema.domain.data_validator import IDataValidator


class ValidateDataSchema:
    """
    Class to validate the data schema in some way by calling the method
    `validate_data` of object IDataValidator. It loads the data and info of dataset
    schema by calling the method `load_data` of objects IDataFileLoader.

    :param data_validator: Object with a method to validate data
    :type data_validator: IDataDownloander
    :param dataset_file_loader: Object with a method to load data
    :type dataset_file_loader: IDataFileLoader
    :param dataset_schema_info_file_loader: Object with a method to load data
    :type dataset_schema_info_file_loader: IDataFileLoader
    """

    def __init__(
        self,
        data_validator: IDataValidator,
        dataset_file_loader: IDataFileLoader,
        dataset_schema_info_file_loader: IDataFileLoader,
    ):
        self.data_validator = data_validator
        self.dataset_file_loader = dataset_file_loader
        self.dataset_schema_info_file_loader = dataset_schema_info_file_loader

    def execute(
        self, dataset_file_path: str, dataset_schema_info_file_path: str
    ) -> None:
        if not os.path.exists(dataset_file_path):
            raise FileNotFoundError(
                f'Dataset file in path "{dataset_file_path}" does notexist'
            )
        if not os.path.exists(dataset_schema_info_file_path):
            raise FileNotFoundError(
                "Dataset schema info file does not exist. Path of the"
                f' file: "{dataset_schema_info_file_path}"'
            )

        dataset = self.dataset_file_loader.load_data(file_path=dataset_file_path)
        dataset_schema_info = self.dataset_schema_info_file_loader.load_data(
            file_path=dataset_schema_info_file_path
        )
        self.data_validator.validate_data(
            dataset=dataset, dataset_schema_info=dataset_schema_info
        )

    @staticmethod
    def build(
        data_validator: IDataValidator,
        dataset_file_loader: IDataFileLoader,
        dataset_schema_info_file_loader: IDataFileLoader,
    ) -> ValidateDataSchema:
        validate_data_schema = ValidateDataSchema(
            data_validator=data_validator,
            dataset_file_loader=dataset_file_loader,
            dataset_schema_info_file_loader=dataset_schema_info_file_loader,
        )
        return validate_data_schema
