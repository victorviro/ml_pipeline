from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.validate_data_schema.application.validate_data_schema_use_case import (
    ValidateDataSchema,
)
from src.validate_data_schema.domain.data_validator import IDataValidator


@pytest.mark.unit
class TestValidateDataSchema:
    mock_data_validator: Mock = Mock(IDataValidator)
    mock_dataset_file_loader: Mock = Mock(IDataFileLoader)
    mock_dataset_schema_info_file_loader: Mock = Mock(IDataFileLoader)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_data_validator = Mock(IDataValidator)
        self.mock_dataset_file_loader = Mock(IDataFileLoader)
        self.mock_dataset_schema_info_file_loader = Mock(IDataFileLoader)

    def test_should_complete_process_returning_success(self):
        use_case = ValidateDataSchema.build(
            data_validator=self.mock_data_validator,
            dataset_file_loader=self.mock_dataset_file_loader,
            dataset_schema_info_file_loader=self.mock_dataset_schema_info_file_loader,
        )
        use_case.execute(
            dataset_file_path=getcwd(), dataset_schema_info_file_path=getcwd()
        )

        self.mock_data_validator.validate_data.assert_called_once()
        self.mock_dataset_file_loader.load_data.assert_called_once()
        self.mock_dataset_schema_info_file_loader.load_data.assert_called_once()

    def test_should_raise_exception_due_non_exist_dataset_file_path(self):
        use_case = ValidateDataSchema.build(
            data_validator=self.mock_data_validator,
            dataset_file_loader=self.mock_dataset_file_loader,
            dataset_schema_info_file_loader=self.mock_dataset_schema_info_file_loader,
        )
        with pytest.raises(Exception):
            use_case.execute(
                dataset_file_path="no_file", dataset_schema_info_file_path=getcwd()
            )

        self.mock_data_validator.validate_data.assert_not_called()
        self.mock_dataset_file_loader.load_data.assert_not_called()
        self.mock_dataset_schema_info_file_loader.load_data.assert_not_called()

    def test_should_raise_exception_due_non_exist_data_schema_path(self):
        use_case = ValidateDataSchema.build(
            data_validator=self.mock_data_validator,
            dataset_file_loader=self.mock_dataset_file_loader,
            dataset_schema_info_file_loader=self.mock_dataset_schema_info_file_loader,
        )
        with pytest.raises(Exception):
            use_case.execute(
                dataset_file_path=getcwd(), dataset_schema_info_file_path="no_file"
            )

        self.mock_data_validator.validate_data.assert_not_called()
        self.mock_dataset_file_loader.load_data.assert_not_called()
        self.mock_dataset_schema_info_file_loader.load_data.assert_not_called()
