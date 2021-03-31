import logging

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.transform_data.domain.data_transformer import IDataTransformer


logger = logging.getLogger(__name__)


class SklearnDataTransformer(IDataTransformer):
    """
    A class which implements the interface IDataTransformer to transform the data.
    It transform the data using a Scikit-learn pipeline fitted previously.
    """

    def transform_data(self, data: dict, transformer_pipeline: Pipeline) -> dict:
        """
        Transform the data using a Scikit-learn pipeline fitted previously.

        :param data: The data to transform
        :type data: dict
        :param transformer_pipeline: The sklearn transformer pipeline
        :type transformer_pipeline: Pipeline
        :return: The data transformed
        :rtype: dict
        """

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
