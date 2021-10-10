from os import getcwd
from unittest.mock import Mock

import pytest

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
from src.transform_data.application.fit_transformer_use_case import FitTransformer
from src.transform_data.domain.transformation_fitter import ITransformationFitter


@pytest.mark.unit
def test_transform_data_should_complete_process_returning_success():
    mock_transformation_fitter = Mock(ITransformationFitter)
    mock_data_file_loader = Mock(IDataFileLoader)
    mock_data_tracker = Mock(IDataTracker)
    mock_data_tracker.track_transformer_fitting_info = Mock()

    use_case = FitTransformer.build(
        data_file_loader=mock_data_file_loader,
        transformation_fitter=mock_transformation_fitter,
        data_tracker=mock_data_tracker,
    )
    use_case.execute(dataset_file_path=getcwd())

    mock_transformation_fitter.fit_transformer.assert_called_once()
    mock_data_file_loader.load_data.assert_called_once()
    mock_data_tracker.track_transformer_fitting_info.assert_called_once()


@pytest.mark.unit
def test_transform_data_use_case_should_raise_exception_due_non_exist_data_file_path():
    mock_transformation_fitter = Mock(ITransformationFitter)
    mock_data_file_loader = Mock(IDataFileLoader)
    mock_data_tracker = Mock(IDataTracker)
    mock_data_tracker.track_transformer_fitting_info = Mock()

    use_case = FitTransformer.build(
        data_file_loader=mock_data_file_loader,
        transformation_fitter=mock_transformation_fitter,
        data_tracker=mock_data_tracker,
    )

    with pytest.raises(Exception):
        use_case.execute(dataset_file_path="no_file")

    mock_transformation_fitter.fit_transformer.assert_not_called()
    mock_data_file_loader.load_data.assert_not_called()
    mock_data_tracker.track_transformer_fitting_info.assert_not_called()
