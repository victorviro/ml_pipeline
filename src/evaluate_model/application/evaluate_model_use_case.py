import os

from src.evaluate_model.domain.model_evaluator import IModelEvaluator
from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker


class EvaluateModel:
    """
    Class to evaluate the model in some way by calling the method
    `evaluate_model` of object IModelEvaluator, and track metrics.

    :param model_evaluator: Object with a method to evaluate the model
    :type model_evaluator: IModelEvaluator
    :param dataset_file_loader: Object with a method to load dataset file
    :type dataset_file_loader: IDataFileLoader
    :param model_file_loader: Object with a method to load model file
    :type model_file_loader: IDataFileLoader
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """
    def __init__(self, model_evaluator: IModelEvaluator,
                 dataset_file_loader: IDataFileLoader,
                 model_file_loader: IDataFileLoader,
                 data_tracker: IDataTracker):
        self.model_evaluator = model_evaluator
        self.dataset_file_loader = dataset_file_loader
        self.model_file_loader = model_file_loader
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str, model_path: str):
        if not os.path.exists(data_file_path):
            raise Exception('Path of dataset file does not exist: '
                            f'"{data_file_path}"')

        # Load the dataset, and the model
        data = self.dataset_file_loader.load_data(file_path=data_file_path)
        model = self.model_file_loader.load_data(file_path=model_path)
        # Evaluate the model
        information_to_track = self.model_evaluator.evaluate_model(
            data=data, model=model
        )
        # Track information
        self.data_tracker.track_model_evaluation_info(
            information_to_track=information_to_track
        )

    @staticmethod
    def build(model_evaluator: IModelEvaluator, dataset_file_loader: IDataFileLoader,
              model_file_loader: IDataFileLoader, data_tracker: IDataTracker):
        evaluate_model = EvaluateModel(model_evaluator=model_evaluator,
                                       dataset_file_loader=dataset_file_loader,
                                       model_file_loader=model_file_loader,
                                       data_tracker=data_tracker)
        return evaluate_model
