import os

from src.validate_model.domain.model_validator import IModelValidator
from src.shared.interfaces.data_file_loader import IDataFileLoader


class ValidateModel:
    """
    Class to validate the model in some way by calling the method
    `validate_data` of object IModelValidator.

    :param model_validator: Object with a method to validate the model
    :type model_validator: IModelValidator
    :param data_file_loader: Object with a method to load data file
    :type data_file_loader: IDataFileLoader
    """
    def __init__(self, model_validator: IModelValidator,
                 data_file_loader: IDataFileLoader):
        self.model_validator = model_validator
        self.data_file_loader = data_file_loader

    def execute(self, data_file_path: str, rmse_threshold: float,
                size_test_split: float, test_split_seed: int):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')
        # Load the dataset
        data: dict = self.data_file_loader.load_data(file_path=data_file_path)
        # Validate the model
        self.model_validator.validate_model(
            data=data, rmse_threshold=rmse_threshold,
            size_test_split=size_test_split, test_split_seed=test_split_seed
        )

    @staticmethod
    def build(model_validator: IModelValidator, data_file_loader: IDataFileLoader):
        validate_model = ValidateModel(model_validator=model_validator,
                                       data_file_loader=data_file_loader)
        return validate_model
