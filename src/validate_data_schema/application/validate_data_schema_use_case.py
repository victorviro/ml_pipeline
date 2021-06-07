import os

from src.validate_data_schema.domain.data_validator import IDataValidator
from src.shared.interfaces.data_file_loader import IDataFileLoader


class ValidateDataSchema:
    """
    Class to validate the data schema in some way by calling the method
    `validate_data` of object IDataValidator. It load the data by calling
    the method `load_data` of object IDataFileLoader.

    :param data_validator: Object with a method to validate data
    :type data_validator: IDataDownloander
    :param data_file_loader: Object with a method to load data
    :type data_file_loader: IDataFileLoader
    """
    def __init__(self, data_validator: IDataValidator, data_file_loader: IDataFileLoader):
        self.data_validator = data_validator
        self.data_file_loader = data_file_loader

    def execute(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Data file in path "{file_path}" does not exist')

        data = self.data_file_loader.load_data(file_path=file_path)
        self.data_validator.validate_data(data=data)

    @staticmethod
    def build(data_validator: IDataValidator, data_file_loader: IDataFileLoader):

        validate_data_schema = ValidateDataSchema(data_validator=data_validator,
                                                  data_file_loader=data_file_loader)
        return validate_data_schema
