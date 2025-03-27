from __future__ import annotations

import os

from src.evaluate_model.domain.model_evaluator import IModelEvaluator
from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker


class EvaluateModel:
    """
    Class to evaluate the model in some way by calling the method
    `evaluate_model` of object IModelEvaluator, and track model metrics.

    :param model_evaluator: Object with a method to evaluate the model
    :type model_evaluator: IModelEvaluator
    :param dataset_file_loader: Object with a method to load dataset file
    :type dataset_file_loader: IDataFileLoader
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """

    def __init__(
        self,
        model_evaluator: IModelEvaluator,
        dataset_file_loader: IDataFileLoader,
        data_tracker: IDataTracker,
    ):
        self.model_evaluator = model_evaluator
        self.dataset_file_loader = dataset_file_loader
        self.data_tracker = data_tracker

    def execute(self, dataset_file_path: str) -> None:
        if not os.path.exists(dataset_file_path):
            raise FileNotFoundError(
                f'Path of dataset file does not exist: "{dataset_file_path}"'
            )

        # Load the dataset, and the model
        dataset = self.dataset_file_loader.load_data(file_path=dataset_file_path)
        model = self.data_tracker.load_model_logged()
        # Evaluate the model
        information_to_log = self.model_evaluator.evaluate_model(
            dataset=dataset, model=model
        )
        # Log information
        self.data_tracker.log_information_of_model_evaluation(
            information_to_log=information_to_log
        )

    @staticmethod
    def build(
        model_evaluator: IModelEvaluator,
        dataset_file_loader: IDataFileLoader,
        data_tracker: IDataTracker,
    ) -> EvaluateModel:
        evaluate_model = EvaluateModel(
            model_evaluator=model_evaluator,
            dataset_file_loader=dataset_file_loader,
            data_tracker=data_tracker,
        )
        return evaluate_model
