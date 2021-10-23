from os import getcwd
from unittest.mock import Mock

import pytest

from src.evaluate_model.application.evaluate_model_use_case import EvaluateModel
from src.evaluate_model.domain.model_evaluator import IModelEvaluator
from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker


@pytest.mark.unit
class TestEvaluateModel:
    mock_model_evaluator: Mock = Mock(IModelEvaluator)
    mock_dataset_file_loader: Mock = Mock(IDataFileLoader)
    mock_data_tracker: Mock = Mock(IDataTracker)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_model_evaluator = Mock(IModelEvaluator)
        self.mock_dataset_file_loader = Mock(IDataFileLoader)
        self.mock_data_tracker = Mock(IDataTracker)

    def test_should_complete_process_returning_success(self):

        use_case = EvaluateModel.build(
            model_evaluator=self.mock_model_evaluator,
            dataset_file_loader=self.mock_dataset_file_loader,
            data_tracker=self.mock_data_tracker,
        )
        use_case.execute(dataset_file_path=getcwd())

        self.mock_dataset_file_loader.load_data.assert_called_once()
        self.mock_data_tracker.load_model_logged.assert_called_once()
        self.mock_model_evaluator.evaluate_model.assert_called_once()
        self.mock_data_tracker.log_information_of_model_evaluation.assert_called_once()

    def test_should_raise_exception_due_non_exist_dataset_file_path(self):

        use_case = EvaluateModel.build(
            model_evaluator=self.mock_model_evaluator,
            dataset_file_loader=self.mock_dataset_file_loader,
            data_tracker=self.mock_data_tracker,
        )

        with pytest.raises(Exception):
            use_case.execute(dataset_file_path="no_file")

        self.mock_dataset_file_loader.load_data.assert_not_called()
        self.mock_data_tracker.load_model_logged.assert_not_called()
        self.mock_model_evaluator.evaluate_model.assert_not_called()
        self.mock_data_tracker.log_information_of_model_evaluation.assert_not_called()
