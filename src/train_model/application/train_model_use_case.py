import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.train_model.domain.model_trainer import IModelTrainer
from src.shared.interfaces.data_tracker import IDataTracker


class TrainModel:
    """
    Class to train and track the model in some way by calling the method
    `train_data` of object IModelTrainer.

    :param model_trainer: Object with a method to train the model
    :type model_trainer: IModelTrainer
    :param data_file_loader: Object with a method to load data file
    :type data_file_loader: IDataFileLoader
    :param data_tracker: Object with a method to track data of the experiment
    :type data_tracker: IDataTracker
    """
    def __init__(self, model_trainer: IModelTrainer,
                 data_file_loader: IDataFileLoader,
                 data_tracker: IDataTracker):
        self.model_trainer = model_trainer
        self.data_file_loader = data_file_loader
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')
        # Load the dataset
        data = self.data_file_loader.load_data(file_path=data_file_path)
        # Train and track the model
        self.model_trainer.train_model(data=data, data_tracker=self.data_tracker)

    @staticmethod
    def build(model_trainer: IModelTrainer, data_file_loader: IDataFileLoader,
              data_tracker: IDataTracker):
        train_model = TrainModel(model_trainer=model_trainer,
                                 data_file_loader=data_file_loader,
                                 data_tracker=data_tracker)
        return train_model
