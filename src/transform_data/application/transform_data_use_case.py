from src.transform_data.domain.data_transformer import IDataTransformer


def transform_data(data_transformer: IDataTransformer, raw_data: dict) -> dict:
    """
    This method transform the data in some way by calling the method
    `transform_data` of object IDataTransformer

    :param data_transformer: Object with a method to transform data
    :type data_transformer: IDataTransformer
    :param raw_data: The data to transform
    :type raw_data: dict
    :return: The data transformed
    :rtype: dict
    """
    if isinstance(data_transformer, IDataTransformer):
        transformed_data = data_transformer.transform_data(raw_data)
        return transformed_data
