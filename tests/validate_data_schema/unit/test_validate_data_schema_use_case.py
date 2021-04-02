from unittest.mock import Mock
from os import getcwd

import pytest

from src.validate_data_schema.application.validate_data_schema_use_case import (
    ValidateDataSchema)
from src.validate_data_schema.domain.data_validator import IDataValidator
from src.shared.interfaces.data_file_loader import IDataFileLoader


@pytest.mark.unit
def test_validate_data_schema_use_case_should_complete_process_returning_success():
    mock_data_validator = Mock(IDataValidator)
    mock_data_validator.validate_data = Mock()

    mock_data_file_loader = Mock(IDataFileLoader)
    mock_data_file_loader.load_data = Mock(return_value={})

    use_case = ValidateDataSchema.build(
        data_validator=mock_data_validator,
        data_file_loader=mock_data_file_loader
    )
    result = use_case.execute(file_path=getcwd())

    mock_data_validator.validate_data.assert_called_once()
    mock_data_file_loader.load_data.assert_called_once()


@pytest.mark.unit
def test_validate_data_schema_use_case_should_raise_exception_due_non_exist_file_path():
    mock_data_validator = Mock(IDataValidator)
    mock_data_file_loader = Mock(IDataFileLoader)

    use_case = ValidateDataSchema.build(
        data_validator=mock_data_validator,
        data_file_loader=mock_data_file_loader
    )
    with pytest.raises(Exception):
        result = use_case.execute(file_path="no_file")

    mock_data_validator.validate_data.assert_not_called()
    mock_data_file_loader.load_data.assert_not_called()
