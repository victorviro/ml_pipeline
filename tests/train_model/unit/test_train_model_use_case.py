from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.model_register import IModelRegister
from src.train_model.application.train_model_use_case import TrainModel
from src.train_model.domain.model_trainer import IModelTrainer


@pytest.mark.unit
class TestTrainModel:
    mock_model_trainer: Mock = Mock(IModelTrainer)
    mock_dataset_file_loader: Mock = Mock(IDataFileLoader)
    mock_data_tracker: Mock = Mock(IDataTracker)
    mock_model_register: Mock = Mock(IModelRegister)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_model_trainer = Mock(IModelTrainer)
        self.mock_dataset_file_loader = Mock(IDataFileLoader)
        self.mock_data_tracker = Mock(IDataTracker)
        self.mock_model_register = Mock(IModelRegister)

    def test_should_complete_process_returning_success(self):
        use_case = TrainModel.build(
            model_trainer=self.mock_model_trainer,
            dataset_file_loader=self.mock_dataset_file_loader,
            data_tracker=self.mock_data_tracker,
            model_register=self.mock_model_register,
            registry_model_name="",
        )
        use_case.execute(dataset_file_path=getcwd())

        self.mock_dataset_file_loader.load_data.assert_called_once()
        self.mock_data_tracker.load_data_preprocessor_logged.assert_called_once()
        self.mock_model_trainer.train_model.assert_called_once()
        self.mock_data_tracker.log_information_of_model_training.assert_called_once()
        self.mock_model_register.register_model.assert_called_once()

    def test_should_raise_exception_due_non_exist_dataset_file_path(self):
        use_case = TrainModel.build(
            model_trainer=self.mock_model_trainer,
            dataset_file_loader=self.mock_dataset_file_loader,
            data_tracker=self.mock_data_tracker,
            model_register=self.mock_model_register,
            registry_model_name="",
        )

        with pytest.raises(Exception):
            use_case.execute(dataset_file_path="no_file")

        self.mock_dataset_file_loader.load_data.assert_not_called()
        self.mock_data_tracker.load_data_preprocessor_logged.assert_not_called()
        self.mock_model_trainer.train_model.assert_not_called()
        self.mock_data_tracker.log_information_of_model_training.assert_not_called()
        self.mock_model_register.register_model.assert_not_called()
