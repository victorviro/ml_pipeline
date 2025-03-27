from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.model_register import IModelRegister
from src.validate_model.application.validate_model_use_case import ValidateModel
from src.validate_model.domain.model_validator import IModelValidator


@pytest.mark.unit
class TestValidateModel:
    mock_model_validator: Mock = Mock(IModelValidator)
    mock_data_tracker: Mock = Mock(IDataTracker)
    mock_model_register: Mock = Mock(IModelRegister)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_model_validator = Mock(IModelValidator)
        self.mock_data_tracker = Mock(IDataTracker)
        self.mock_model_register = Mock(IModelRegister)

    def test_should_complete_process_returning_success(self):
        use_case = ValidateModel.build(
            model_validator=self.mock_model_validator,
            data_tracker=self.mock_data_tracker,
            model_register=self.mock_model_register,
            registry_model_name="",
        )
        use_case.execute(metrics_threshold={})

        mock_data_tracker = self.mock_data_tracker
        mock_data_tracker.get_information_logged_for_model_validation.assert_called_once()
        self.mock_model_validator.validate_model.assert_called_once()
        self.mock_model_register.transition_model_version_stage.assert_called_once()

    def test_should_raise_exception_due_to_no_metrics_tracked(self):
        self.mock_data_tracker.get_information_logged_for_model_validation = Mock(
            return_value={}
        )

        use_case = ValidateModel.build(
            model_validator=self.mock_model_validator,
            data_tracker=self.mock_data_tracker,
            model_register=self.mock_model_register,
            registry_model_name="",
        )

        with pytest.raises(Exception):
            use_case.execute(metrics_threshold={})

        mock_data_tracker = self.mock_data_tracker
        mock_data_tracker.get_information_logged_for_model_validation.assert_called_once()
        self.mock_model_validator.validate_model.assert_not_called()
        self.mock_model_register.transition_model_version_stage.assert_not_called()

    def test_should_raise_exception_due_to_no_model_validated(self):
        self.mock_model_validator.validate_model = Mock(return_value=False)

        use_case = ValidateModel.build(
            model_validator=self.mock_model_validator,
            data_tracker=self.mock_data_tracker,
            model_register=self.mock_model_register,
            registry_model_name="",
        )

        with pytest.raises(Exception):
            use_case.execute(metrics_threshold={})

        mock_data_tracker = self.mock_data_tracker
        mock_data_tracker.get_information_logged_for_model_validation.assert_called_once()
        self.mock_model_validator.validate_model.assert_called_once()
        self.mock_model_register.transition_model_version_stage.assert_not_called()
