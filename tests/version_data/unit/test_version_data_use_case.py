from unittest.mock import Mock
from os import getcwd

import pytest

from src.version_data.application.version_data_use_case import VersionData
from src.version_data.domain.data_versioner import IDataVersioner


@pytest.mark.unit
def test_version_data_use_case_should_complete_process_returning_success():
    mock_data_versioner = Mock(IDataVersioner)
    mock_data_versioner.version_data = Mock()

    use_case = VersionData.build(data_versioner=mock_data_versioner)
    result = use_case.execute(data_file_path=getcwd(), data_version=0)

    mock_data_versioner.version_data.assert_called_once()


@pytest.mark.unit
def test_version_data_use_case_should_raise_exception_due_non_exist_data_file_path():
    mock_data_versioner = Mock(IDataVersioner)

    use_case = VersionData.build(data_versioner=mock_data_versioner)

    with pytest.raises(Exception):
        result = use_case.execute(file_path="no_file")

    mock_data_versioner.version_data.assert_not_called()
