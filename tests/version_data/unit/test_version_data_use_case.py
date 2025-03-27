from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_tracker import IDataTracker
from src.version_data.application.version_data_use_case import VersionTrackData
from src.version_data.domain.data_versioner import IDataVersioner


@pytest.mark.unit
class TestVersionTrackData:
    mock_data_versioner: Mock = Mock(IDataVersioner)
    mock_data_tracker: Mock = Mock(IDataTracker)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_data_versioner = Mock(IDataVersioner)
        self.mock_data_tracker = Mock(IDataTracker)

    def test_should_complete_process_returning_success(self):
        use_case = VersionTrackData.build(
            data_versioner=self.mock_data_versioner, data_tracker=self.mock_data_tracker
        )
        use_case.execute(data_file_path=getcwd(), data_version=0)

        self.mock_data_versioner.version_data.assert_called_once()
        self.mock_data_tracker.log_information_of_data_versioning.assert_called_once()

    def test_should_raise_exception_due_non_exist_data_file_path(self):
        use_case = VersionTrackData.build(
            data_versioner=self.mock_data_versioner, data_tracker=self.mock_data_tracker
        )

        with pytest.raises(Exception):
            use_case.execute(data_file_path="no_file", data_version=0)

        self.mock_data_versioner.version_data.assert_not_called()
        self.mock_data_tracker.log_information_of_data_versioning.assert_not_called()
