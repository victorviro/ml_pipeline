from os import getcwd
from unittest.mock import Mock

import pytest

from src.get_data.application.get_data_use_case import GetData
from src.get_data.domain.data_downloander import IDataDownloander
from src.get_data.domain.data_file_saver import IDataFileSaver


@pytest.mark.unit
def test_get_data_use_case_should_complete_process_returning_success():
    mock_data_downloander = Mock(IDataDownloander)
    mock_data_downloander.download_data = Mock()

    mock_data_file_saver = Mock(IDataFileSaver)
    mock_data_file_saver.save_data = Mock()

    use_case = GetData.build(
        data_downloander=mock_data_downloander,
        data_file_saver=mock_data_file_saver
    )
    use_case.execute(file_path=getcwd())

    mock_data_downloander.download_data.assert_called_once()
    mock_data_file_saver.save_data.assert_called_once()


@pytest.mark.unit
def test_get_data_use_case_should_raise_exception_due_non_exist_data_path():
    mock_data_downloander = Mock(IDataDownloander)
    mock_data_downloander.download_data = Mock()

    mock_data_file_saver = Mock(IDataFileSaver)

    use_case = GetData.build(
        data_downloander=mock_data_downloander,
        data_file_saver=mock_data_file_saver
    )
    with pytest.raises(Exception):
        use_case.execute(file_path="no_path/no_file")

    mock_data_downloander.download_data.assert_not_called()
    mock_data_file_saver.save_data.assert_not_called()


@pytest.mark.unit
def test_get_data_use_case_should_raise_exception_due_non_exist_data_file_path():
    mock_data_downloander = Mock(IDataDownloander)
    mock_data_downloander.download_data = Mock()

    mock_data_file_saver = Mock(IDataFileSaver)
    mock_data_file_saver.save_data = Mock()

    use_case = GetData.build(
        data_downloander=mock_data_downloander,
        data_file_saver=mock_data_file_saver
    )
    with pytest.raises(Exception):
        use_case.execute(file_path=f"{getcwd()}/no_file")

    mock_data_downloander.download_data.assert_called_once()
    mock_data_file_saver.save_data.assert_called_once()
