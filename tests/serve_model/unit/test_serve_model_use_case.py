from unittest.mock import Mock

import pytest

from src.serve_model.application.serve_model_use_case import ServeModel
from src.serve_model.domain.model_server import IModelServer
from src.shared.interfaces.data_tracker import IDataTracker


@pytest.mark.unit
class TestEvaluateModel:
    mock_model_server: Mock = Mock(IModelServer)
    mock_data_tracker: Mock = Mock(IDataTracker)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_model_server = Mock(IModelServer)
        self.mock_data_tracker = Mock(IDataTracker)

    def test_should_complete_process_returning_success(self):
        use_case = ServeModel.build(
            model_server=self.mock_model_server,
            data_tracker=self.mock_data_tracker,
            model_version=1.0,
        )
        use_case.execute()

        self.mock_data_tracker.get_model_path_in_storage.assert_called_once()
        self.mock_model_server.serve_model.assert_called_once()
