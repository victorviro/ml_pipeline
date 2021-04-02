import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.transform_data.domain.data_transformer import IDataTransformer
from src.shared.interfaces.data_file_loader import IDataFileLoader


logger = logging.getLogger(__name__)


class SklearnDataTransformer(IDataTransformer):
    """
    A class which implements the interface IDataTransformer to transform the data.
    It transform the data using a Scikit-learn pipeline fitted previously.

    :param transformer_pipeline: The sklearn transformer pipeline
    :type transformer_pipeline: Pipeline
    """
    def __init__(self, transformer_file_path: str):
        self.transformer_file_path = transformer_file_path

    def transform_data(self, data: dict, data_file_loader: IDataFileLoader) -> dict:
        """
        Transform the data using a Scikit-learn pipeline fitted previously.

        :param data: The data to transform
        :type data: dict
        :return: The data transformed
        :rtype: dict
        """
        # Load transfomer pipeline
        try:
            transformer_pipeline: Pipeline = data_file_loader.load_data(
                file_path=self.transformer_file_path
            )
        except Exception as err:
            msg = f'Error loading transformer pipeline. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)
        try:
            # Load data to pandas DataFrame
            data_df = DataFrame(data)
            data_columns = data_df.columns.to_list()
            data_columns.append('ratio_cols_rows')
            # Transform the dataset
            data_tranformed_array = transformer_pipeline.transform(data_df)
            data_transformed_df = DataFrame(data_tranformed_array,
                                            columns=data_columns)
            data_transformed = data_transformed_df.to_dict(orient='list')
        except Exception as err:
            msg = f'Error when transforming data. Traceback: {err}'
            logger.error(msg)
            raise Exception(msg)

        return data_transformed
