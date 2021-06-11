from unittest.mock import Mock
from os import getcwd

import pytest

from src.version_data.application.version_data_use_case import VersionTrackData
from src.version_data.domain.data_versioner import IDataVersioner
from src.shared.interfaces.data_tracker import IDataTracker


@pytest.mark.unit
def test_version_data_use_case_should_complete_process_returning_success():
    mock_data_versioner = Mock(IDataVersioner)
    mock_data_versioner.version_data = Mock(return_value={})

    mock_data_tracker = Mock(IDataTracker)
    mock_data_tracker.track_items = Mock()

    use_case = VersionTrackData.build(data_versioner=mock_data_versioner,
                                      data_tracker=mock_data_tracker)
    use_case.execute(data_file_path=getcwd(), data_version=0)

    mock_data_versioner.version_data.assert_called_once()
    mock_data_tracker.track_items.assert_called_once()


@pytest.mark.unit
def test_version_data_use_case_should_raise_exception_due_non_exist_data_file_path():
    mock_data_versioner = Mock(IDataVersioner)
    mock_data_versioner.version_data = Mock(return_value={})
    mock_data_tracker = Mock(IDataTracker)
    mock_data_tracker.track_items = Mock()

    use_case = VersionTrackData.build(data_versioner=mock_data_versioner,
                                      data_tracker=mock_data_tracker)

    with pytest.raises(Exception):
        use_case.execute(file_path="no_file")

    mock_data_versioner.version_data.assert_not_called()
    mock_data_tracker.track_items.assert_not_called()
