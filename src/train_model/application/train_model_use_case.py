import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.train_model.domain.model_trainer import IModelTrainer
from src.shared.interfaces.data_tracker import IDataTracker


class TrainModel:
    """
    Class to train the model by calling the method `train_data` of object IModelTrainer.
    It firts loads the data and the transformer files. Finally, it tracks information.

    :param model_trainer: Object with a method to train the model
    :type model_trainer: IModelTrainer
    :param dataset_file_loader: Object with a method to load data file
    :type dataset_file_loader: IDataFileLoader
    :param data_tracker: Object with a method to track data of the experiment
    :type data_tracker: IDataTracker
    :param transformer_file_loader: Object with a method to load data file
    :type transformer_file_loader: IDataFileLoader
    """
    def __init__(self, model_trainer: IModelTrainer,
                 dataset_file_loader: IDataFileLoader,
                 data_tracker: IDataTracker,
                 transformer_file_loader: IDataFileLoader):
        self.model_trainer = model_trainer
        self.dataset_file_loader = dataset_file_loader
        self.data_tracker = data_tracker
        self.transformer_file_loader = transformer_file_loader

    def execute(self, data_file_path: str, transformer_file_path: str):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')
        if not os.path.exists(transformer_file_path):
            raise Exception('Path of transformer file does not exist: '
                            f'"{transformer_file_path}"')
        # Load the dataset and transformer files
        data = self.dataset_file_loader.load_data(file_path=data_file_path)
        transformer = self.transformer_file_loader.load_data(
            file_path=transformer_file_path
        )
        # Train the model
        information_to_track = self.model_trainer.train_model(data=data,
                                                              transformer=transformer)
        # Track information of the experiment run
        self.data_tracker.track_training_info(information_to_track)

    @staticmethod
    def build(model_trainer: IModelTrainer, dataset_file_loader: IDataFileLoader,
              data_tracker: IDataTracker, transformer_file_loader: IDataFileLoader):
        train_model = TrainModel(model_trainer=model_trainer,
                                 dataset_file_loader=dataset_file_loader,
                                 data_tracker=data_tracker,
                                 transformer_file_loader=transformer_file_loader)
        return train_model
