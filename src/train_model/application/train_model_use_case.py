import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.model_register import IModelRegister
from src.train_model.domain.model_trainer import IModelTrainer


class TrainModel:
    """
    Class to train the model by calling the method `train_data` of object IModelTrainer.
    It first loads the dataset and gets the transformer tracked. Finally, it tracks
    information.

    :param model_trainer: Object with a method to train the model
    :type model_trainer: IModelTrainer
    :param dataset_file_loader: Object with a method to load data file
    :type dataset_file_loader: IDataFileLoader
    :param data_tracker: Object with a method to track data of the experiment
    :type data_tracker: IDataTracker
    """

    def __init__(
        self,
        model_trainer: IModelTrainer,
        dataset_file_loader: IDataFileLoader,
        data_tracker: IDataTracker,
        model_register: IModelRegister,
        registry_model_name: str,
        data_preprocessor_name: str,
    ):
        self.model_trainer = model_trainer
        self.dataset_file_loader = dataset_file_loader
        self.data_tracker = data_tracker
        self.model_register = model_register
        self.registry_model_name = registry_model_name
        self.data_preprocessor_name = data_preprocessor_name

    def execute(self, dataset_file_path: str):
        if not os.path.exists(dataset_file_path):
            raise Exception(f"Path of dataset file does not exist: {dataset_file_path}")
        # Load the dataset
        dataset = self.dataset_file_loader.load_data(file_path=dataset_file_path)
        # Get the preprocesser logged
        data_preprocessor = self.data_tracker.load_model_logged(
            model_name=self.data_preprocessor_name
        )
        # Train the model
        information_to_log = self.model_trainer.train_model(
            dataset=dataset, preprocesser=data_preprocessor
        )
        # Track information of the experiment run
        self.data_tracker.log_information_of_model_training(
            information_to_log=information_to_log
        )
        # Register the model in Model Registry
        self.model_register.register_model(name=self.registry_model_name)

    @staticmethod
    def build(
        model_trainer: IModelTrainer,
        dataset_file_loader: IDataFileLoader,
        data_tracker: IDataTracker,
        model_register: IModelRegister,
        registry_model_name: str,
        data_preprocessor_name: str,
    ):
        train_model = TrainModel(
            model_trainer=model_trainer,
            dataset_file_loader=dataset_file_loader,
            data_tracker=data_tracker,
            model_register=model_register,
            registry_model_name=registry_model_name,
            data_preprocessor_name=data_preprocessor_name,
        )
        return train_model
