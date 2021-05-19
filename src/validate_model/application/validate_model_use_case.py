import os

from src.validate_model.domain.model_validator import IModelValidator
from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker


class ValidateModel:
    """
    Class to validate the model in some way by calling the method
    `validate_data` of object IModelValidator. And update its stage
    in Model Registry if its validation succeds.

    :param model_validator: Object with a method to validate the model
    :type model_validator: IModelValidator
    :param dataset_file_loader: Object with a method to load dataset file
    :type dataset_file_loader: IDataFileLoader
    :param model_file_loader: Object with a method to load model file
    :type model_file_loader: IDataFileLoader
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """
    def __init__(self, model_validator: IModelValidator,
                 dataset_file_loader: IDataFileLoader,
                 model_file_loader: IDataFileLoader,
                 data_tracker: IDataTracker):
        self.model_validator = model_validator
        self.dataset_file_loader = dataset_file_loader
        self.model_file_loader = model_file_loader
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str, model_path: str):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')

        # Load the dataset, and the pipeline
        data = self.dataset_file_loader.load_data(file_path=data_file_path)
        model = self.model_file_loader.load_data(file_path=model_path)
        # Validate the model
        self.model_validator.validate_model(data=data, model=model)
        # Update model's stage in Model Registry
        self.data_tracker.update_validated_model_in_registry()

    @staticmethod
    def build(model_validator: IModelValidator, dataset_file_loader: IDataFileLoader,
              model_file_loader: IDataFileLoader, data_tracker: IDataTracker):
        validate_model = ValidateModel(model_validator=model_validator,
                                       dataset_file_loader=dataset_file_loader,
                                       model_file_loader=model_file_loader,
                                       data_tracker=data_tracker)
        return validate_model
