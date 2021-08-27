import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
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
    ):
        self.model_trainer = model_trainer
        self.dataset_file_loader = dataset_file_loader
        self.data_tracker = data_tracker

    def execute(self, dataset_file_path: str):
        if not os.path.exists(dataset_file_path):
            raise Exception(
                "Path of dataset file does not exist: " f'"{dataset_file_path}"'
            )
        # Load the dataset
        dataset = self.dataset_file_loader.load_data(file_path=dataset_file_path)
        # Get the transformer tracked
        transformer = self.data_tracker.get_tracked_transformer()
        # Train the model
        information_to_track = self.model_trainer.train_model(
            dataset=dataset, transformer=transformer
        )
        # Track information of the experiment run
        self.data_tracker.track_training_info(information_to_track)

    @staticmethod
    def build(
        model_trainer: IModelTrainer,
        dataset_file_loader: IDataFileLoader,
        data_tracker: IDataTracker,
    ):
        train_model = TrainModel(
            model_trainer=model_trainer,
            dataset_file_loader=dataset_file_loader,
            data_tracker=data_tracker,
        )
        return train_model
