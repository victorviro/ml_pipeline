from src.core import IDataDownloander, IDataValidator, IDataTransformer


def download_data(data_downloander: IDataDownloander):
    if isinstance(data_downloander, IDataDownloander):
        data_downloander.download_data()


def validate_schema(data_validator: IDataValidator):
    if isinstance(data_validator, IDataValidator):
        data_validator.validate_data()


def transform_data(data_transformer: IDataTransformer):
    if isinstance(data_transformer, IDataTransformer):
        data_transformer.transform_data()
