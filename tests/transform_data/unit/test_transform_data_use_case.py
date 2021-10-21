from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
from src.transform_data.application.fit_transformer_use_case import FitTransformer
from src.transform_data.domain.transformation_fitter import ITransformationFitter


@pytest.mark.unit
class TestFitTransformer:
    mock_transformation_fitter: Mock = Mock(ITransformationFitter)
    mock_data_file_loader: Mock = Mock(IDataFileLoader)
    mock_data_tracker: Mock = Mock(IDataTracker)

    def setup(self) -> None:
        self.reset_mock()

    def reset_mock(self) -> None:
        self.mock_transformation_fitter = Mock(ITransformationFitter)
        self.mock_data_file_loader = Mock(IDataFileLoader)
        self.mock_data_tracker = Mock(IDataTracker)

    def test_should_complete_process_returning_success(self):

        use_case = FitTransformer.build(
            data_file_loader=self.mock_data_file_loader,
            transformation_fitter=self.mock_transformation_fitter,
            data_tracker=self.mock_data_tracker,
        )
        use_case.execute(dataset_file_path=getcwd())

        self.mock_transformation_fitter.fit_transformer.assert_called_once()
        self.mock_data_file_loader.load_data.assert_called_once()
        m_data_tracker = self.mock_data_tracker
        m_data_tracker.log_information_of_data_preprocessor_fitting.assert_called_once()

    def test_should_raise_exception_due_non_exist_data_file_path(self):

        use_case = FitTransformer.build(
            data_file_loader=self.mock_data_file_loader,
            transformation_fitter=self.mock_transformation_fitter,
            data_tracker=self.mock_data_tracker,
        )

        with pytest.raises(Exception):
            use_case.execute(dataset_file_path="no_file")

        self.mock_transformation_fitter.fit_transformer.assert_not_called()
        self.mock_data_file_loader.load_data.assert_not_called()
        m_data_tracker = self.mock_data_tracker
        m_data_tracker.log_information_of_data_preprocessor_fitting.assert_not_called()
