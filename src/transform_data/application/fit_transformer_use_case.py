import os

from src.transform_data.domain.transformation_fitter import ITransformationFitter
from src.shared.interfaces.data_file_saver import IDataFileSaver
from src.shared.interfaces.data_file_loader import IDataFileLoader


class FitTransformer:
    """
    Class to fit a transformer in some way by calling the method
    `fit_transfomer` of object ITransformationFitter.

    :param data_file_loader: Object with a method to load a data file
    :type data_file_loader: IDataFileLoader
    :param transformation_fitter: Object with a method to fit a transformer
    :type transformation_fitter: ITransformationFitter
    :param data_file_saver: Object with a method to save data to a file
    :type data_file_saver: IDataFileSaver
    """
    def __init__(self, data_file_loader: IDataFileLoader,
                 transformation_fitter: ITransformationFitter,
                 data_file_saver: IDataFileSaver):
        self.data_file_loader = data_file_loader
        self.transformation_fitter = transformation_fitter
        self.data_file_saver = data_file_saver

    def execute(self, data_file_path: dict, transformer_file_path: str,
                size_test_split: float, test_split_seed: int) -> dict:
        # Load the dataset
        data: dict = self.data_file_loader.load_data(file_path=data_file_path)
        # Fit the transformer pipeline
        transformer_pipeline = self.transformation_fitter.fit_transformer(
            data=data, size_test_split=size_test_split, test_split_seed=test_split_seed
        )
        if not os.path.exists(os.path.dirname(transformer_file_path)):
            raise Exception('Path where save transformer pipeline file does not exist: '
                            f'"{os.path.dirname(transformer_file_path)}"')
        # Save the transformer pipeline
        self.data_file_saver.save_data(
            file_path=transformer_file_path,
            file=transformer_pipeline
        )
        if not os.path.exists(transformer_file_path):
            raise Exception('Path of transformer pipeline file does not exist: '
                            f'"{transformer_file_path}"')

    @staticmethod
    def build(data_file_loader: IDataFileLoader,
              transformation_fitter: ITransformationFitter,
              data_file_saver: IDataFileSaver):
        fit_transformer = FitTransformer(data_file_loader=data_file_loader,
                                         transformation_fitter=transformation_fitter,
                                         data_file_saver=data_file_saver)
        return fit_transformer
