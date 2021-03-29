import os

from pandera import DataFrameSchema

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

    def execute(self, file_path: str, data_schema: DataFrameSchema):
        if not os.path.exists(file_path):
            raise Exception(f'File in path {file_path} does not exist')
        data: dict = self.data_file_loader.load_data(file_path=file_path)
        if not isinstance(data, dict):
            raise Exception(f'Data loaded is not a dict. It is a {type(data)}')
        self.data_validator.validate_data(data=data, data_schema=data_schema)

    @staticmethod
    def build(data_validator: IDataValidator,
              data_file_loader: IDataFileLoader):

        validate_data_schema = ValidateDataSchema(
            data_validator=data_validator,
            data_file_loader=data_file_loader
        )
        return validate_data_schema
