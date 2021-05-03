import os

from src.transform_data.domain.transformation_fitter import ITransformationFitter
from src.shared.interfaces.data_file_saver import IDataFileSaver
from src.shared.interfaces.data_file_loader import IDataFileLoader
from src.shared.interfaces.data_tracker import IDataTracker


class FitTransformer:
    """
    Class to fit and track a transformer in some way by calling the method
    `fit_transfomer` of object ITransformationFitter.

    :param data_file_loader: Object with a method to load a data file
    :type data_file_loader: IDataFileLoader
    :param transformation_fitter: Object with a method to fit a transformer
    :type transformation_fitter: ITransformationFitter
    :param data_file_saver: Object with a method to save data to a file
    :type data_file_saver: IDataFileSaver
    :param data_tracker: Object with a method to track data to an experiment
    :type data_tracker: IDataTracker
    """
    def __init__(self, data_file_loader: IDataFileLoader,
                 transformation_fitter: ITransformationFitter,
                 data_file_saver: IDataFileSaver,
                 data_tracker: IDataTracker):
        self.data_file_loader = data_file_loader
        self.transformation_fitter = transformation_fitter
        self.data_file_saver = data_file_saver
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str, transformer_file_path: str):
        if not os.path.exists(data_file_path):
            raise Exception(f'Path of data file does not exist: "{data_file_path}"')
        # Load the dataset
        data = self.data_file_loader.load_data(file_path=data_file_path)

        if not os.path.exists(os.path.dirname(transformer_file_path)):
            raise Exception('Path where save transformer pipeline file does not exist: '
                            f'"{os.path.dirname(transformer_file_path)}"')
        # Fit and track the transformer pipeline
        self.transformation_fitter.fit_transformer(
            data=data,
            data_file_saver=self.data_file_saver,
            data_tracker=self.data_tracker
        )

    @staticmethod
    def build(data_file_loader: IDataFileLoader,
              transformation_fitter: ITransformationFitter,
              data_file_saver: IDataFileSaver,
              data_tracker: IDataTracker):
        fit_transformer = FitTransformer(data_file_loader=data_file_loader,
                                         transformation_fitter=transformation_fitter,
                                         data_file_saver=data_file_saver,
                                         data_tracker=data_tracker)
        return fit_transformer
