import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.train_model.domain.model_trainer import IModelTrainer


class TrainModel:
    """
    Class to train the model in some way by calling the method
    `train_data` of object IModelTrainer.

    :param model_trainer: Object with a method to train the model
    :type model_trainer: IModelTrainer
    :param data_file_loader: Object with a method to load data file
    :type data_file_loader: IDataFileLoader
    """
    def __init__(self, model_trainer: IModelTrainer,
                 data_file_loader: IDataFileLoader):
        self.model_trainer = model_trainer
        self.data_file_loader = data_file_loader

    def execute(self, data_file_path: str, transformer_pipe_path: str,
                transformer_name: str, size_test_split: float, test_split_seed: int,
                alpha: float, l1_ratio: float, model_seed: int, model_name: str):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')
        # Load the dataset
        data: dict = self.data_file_loader.load_data(file_path=data_file_path)
        # Train the model
        self.model_trainer.train_model(
            data=data, transformer_pipe_path=transformer_pipe_path,
            transformer_name=transformer_name, size_test_split=size_test_split,
            test_split_seed=test_split_seed, alpha=alpha, l1_ratio=l1_ratio,
            model_seed=model_seed, model_name=model_name
        )

    @staticmethod
    def build(model_trainer: IModelTrainer, data_file_loader: IDataFileLoader):
        train_model = TrainModel(model_trainer=model_trainer,
                                 data_file_loader=data_file_loader)
        return train_model
