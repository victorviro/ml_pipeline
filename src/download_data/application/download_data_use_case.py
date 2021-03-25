import requests

from src.download_data.domain.data_downloander import IDataDownloander


def download_data(data_downloander: IDataDownloander):
    """
    This method download the data in some way calling the method
    `download_data` of object IDataDownloander

    :param data_downloander: Object with a method to download data
    :type data_downloander: IDataDownloander
    """
    if isinstance(data_downloander, IDataDownloander):
        data_downloander.download_data()
