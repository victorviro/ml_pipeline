from src.version_data.domain.data_versioner import IDataVersioner


def version_data(data_versioner: IDataVersioner):
    if isinstance(data_versioner, IDataVersioner):
        data_versioner.version_data()
