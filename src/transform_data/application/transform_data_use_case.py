import os

from src.transform_data.domain.data_transformer import IDataTransformer
from src.shared.interfaces.data_file_loader import IDataFileLoader


class TransformData:
    """
    Class to transform the data in some way by calling the method
    `transform_data` of object IDataTransformer.

    :param data_transformer: Object with a method to download data
    :type data_transformer: IDataTransformer
    :param data_file_loader: Object with a method to load data file
    :type data_file_loader: IDataFileLoader
    """
    def __init__(self, data_transformer: IDataTransformer,
                 data_file_loader: IDataFileLoader):
        self.data_transformer = data_transformer
        self.data_file_loader = data_file_loader

    def execute(self, data: dict, transformer_file_path: str) -> dict:
        if not os.path.exists(transformer_file_path):
            raise Exception('Path of transformer pipeline file does not exist: '
                            f'"{transformer_file_path}"')
        # Load the transformer pipeline
        transformer_pipeline = self.data_file_loader.load_data(
            file_path=transformer_file_path
        )
        # Tranform the dataset
        data_transformed = self.data_transformer.transform_data(
            data=data,
            transformer_pipeline=transformer_pipeline
        )
        return data_transformed

    @staticmethod
    def build(data_transformer: IDataTransformer, data_file_loader: IDataFileLoader):
        transform_data = TransformData(data_transformer=data_transformer,
                                       data_file_loader=data_file_loader)
        return transform_data
