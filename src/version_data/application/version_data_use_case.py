from src.version_data.domain.data_versioner import IDataVersioner


def version_data(data_versioner: IDataVersioner):
    """
    This method version the data in some way calling the method
    `version_data` of object IDataVersioner

    :param data_versioner: Object with a method to version data
    :type data_versioner: IDataVersioner
    """
    if isinstance(data_versioner, IDataVersioner):
        data_versioner.version_data()
