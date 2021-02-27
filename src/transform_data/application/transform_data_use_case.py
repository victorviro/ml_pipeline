from src.transform_data.domain.data_transformer import IDataTransformer


def transform_data(data_transformer: IDataTransformer):
    if isinstance(data_transformer, IDataTransformer):
        data_transformer.transform_data()
