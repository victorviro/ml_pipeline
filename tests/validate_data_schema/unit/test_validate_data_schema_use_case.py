from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.validate_data_schema.application.validate_data_schema_use_case import (
    ValidateDataSchema,
)
from src.validate_data_schema.domain.data_validator import IDataValidator


@pytest.mark.unit
def test_validate_data_schema_should_complete_process_returning_success():
    mock_data_validator = Mock(IDataValidator)
    mock_data_validator.validate_data = Mock()

    mock_dataset_file_loader = Mock(IDataFileLoader)
    mock_dataset_file_loader.load_data = Mock(return_value={})
    mock_dataset_schema_info_file_loader = Mock(IDataFileLoader)
    mock_dataset_schema_info_file_loader.load_data = Mock(return_value={})

    use_case = ValidateDataSchema.build(
        data_validator=mock_data_validator,
        dataset_file_loader=mock_dataset_file_loader,
        dataset_schema_info_file_loader=mock_dataset_schema_info_file_loader
    )
    use_case.execute(
        dataset_file_path=getcwd(),
        dataset_schema_info_file_path=getcwd()
    )

    mock_data_validator.validate_data.assert_called_once()
    mock_dataset_file_loader.load_data.assert_called_once()
    mock_dataset_schema_info_file_loader.load_data.assert_called_once()


@pytest.mark.unit
def test_validate_data_schema_should_raise_exception_due_non_exist_dataset_file_path():
    mock_data_validator = Mock(IDataValidator)
    mock_dataset_file_loader = Mock(IDataFileLoader)
    mock_dataset_schema_info_file_loader = Mock(IDataFileLoader)

    use_case = ValidateDataSchema.build(
        data_validator=mock_data_validator,
        dataset_file_loader=mock_dataset_file_loader,
        dataset_schema_info_file_loader=mock_dataset_schema_info_file_loader
    )
    with pytest.raises(Exception):
        use_case.execute(
            dataset_file_path="no_file",
            dataset_schema_info_file_path=getcwd()
        )

    mock_data_validator.validate_data.assert_not_called()
    mock_dataset_file_loader.load_data.assert_not_called()
    mock_dataset_schema_info_file_loader.load_data.assert_not_called()


@pytest.mark.unit
def test_validate_data_schema_should_raise_exception_due_non_exist_data_schema_path():
    mock_data_validator = Mock(IDataValidator)
    mock_dataset_file_loader = Mock(IDataFileLoader)
    mock_dataset_schema_info_file_loader = Mock(IDataFileLoader)

    use_case = ValidateDataSchema.build(
        data_validator=mock_data_validator,
        dataset_file_loader=mock_dataset_file_loader,
        dataset_schema_info_file_loader=mock_dataset_schema_info_file_loader
    )
    with pytest.raises(Exception):
        use_case.execute(
            dataset_file_path=getcwd(),
            dataset_schema_info_file_path="no_file"
        )

    mock_data_validator.validate_data.assert_not_called()
    mock_dataset_file_loader.load_data.assert_not_called()
    mock_dataset_schema_info_file_loader.load_data.assert_not_called()
