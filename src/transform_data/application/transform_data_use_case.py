from src.transform_data.domain.data_transformer import IDataTransformer


def transform_data(data_transformer: IDataTransformer, raw_data, transformer_pipe):
    if isinstance(data_transformer, IDataTransformer):
        transformed_data = data_transformer.transform_data(raw_data, transformer_pipe)
        return transformed_data
