from os import getcwd
from unittest.mock import Mock

import pytest

from src.get_data.application.get_data_use_case import GetData
from src.get_data.domain.data_downloander import IDataDownloander
from src.get_data.domain.data_file_saver import IDataFileSaver


@pytest.mark.unit
class TestGetData:
    mock_data_downloander: Mock = Mock(IDataDownloander)
    mock_data_file_saver: Mock = Mock(IDataFileSaver)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_data_downloander = Mock(IDataDownloander)
        self.mock_data_file_saver = Mock(IDataFileSaver)

    def test_should_complete_process_returning_success(self):

        use_case = GetData.build(
            data_downloander=self.mock_data_downloander,
            data_file_saver=self.mock_data_file_saver,
        )
        use_case.execute(file_path=getcwd())

        self.mock_data_downloander.download_data.assert_called_once()
        self.mock_data_file_saver.save_data.assert_called_once()

    def test_should_raise_exception_due_non_exist_data_path(self):

        use_case = GetData.build(
            data_downloander=self.mock_data_downloander,
            data_file_saver=self.mock_data_file_saver,
        )
        with pytest.raises(Exception):
            use_case.execute(file_path="no_path/no_file")

        self.mock_data_downloander.download_data.assert_not_called()
        self.mock_data_file_saver.save_data.assert_not_called()

    def test_should_raise_exception_due_non_exist_data_file_path(self):
        use_case = GetData.build(
            data_downloander=self.mock_data_downloander,
            data_file_saver=self.mock_data_file_saver,
        )
        with pytest.raises(Exception):
            use_case.execute(file_path=f"{getcwd()}/no_file")

        self.mock_data_downloander.download_data.assert_called_once()
        self.mock_data_file_saver.save_data.assert_called_once()
