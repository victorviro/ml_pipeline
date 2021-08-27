import os

from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker
from src.transform_data.domain.transformation_fitter import ITransformationFitter


class FitTransformer:
    """
    Class to fit and track a transformer in some way by calling the method
    `fit_transfomer` of object ITransformationFitter.

    :param data_file_loader: Object with a method to load a data file
    :type data_file_loader: IDataFileLoader
    :param transformation_fitter: Object with a method to fit a transformer
    :type transformation_fitter: ITransformationFitter
    :param data_tracker: Object with a method to track data to an experiment
    :type data_tracker: IDataTracker
    """

    def __init__(
        self,
        data_file_loader: IDataFileLoader,
        transformation_fitter: ITransformationFitter,
        data_tracker: IDataTracker,
    ):
        self.data_file_loader = data_file_loader
        self.transformation_fitter = transformation_fitter
        self.data_tracker = data_tracker

    def execute(self, dataset_file_path: str):
        if not os.path.exists(dataset_file_path):
            raise FileNotFoundError(
                "Path of the dataset file does not exist: " f'"{dataset_file_path}"'
            )
        # Load the dataset
        dataset = self.data_file_loader.load_data(file_path=dataset_file_path)

        # Fit the transformer/prepocessing
        transformer = self.transformation_fitter.fit_transformer(dataset=dataset)

        # Track the transformer and information
        self.data_tracker.track_transformer_fitting_info(transformer=transformer)

    @staticmethod
    def build(
        data_file_loader: IDataFileLoader,
        transformation_fitter: ITransformationFitter,
        data_tracker: IDataTracker,
    ):
        fit_transformer = FitTransformer(
            data_file_loader=data_file_loader,
            transformation_fitter=transformation_fitter,
            data_tracker=data_tracker,
        )
        return fit_transformer
