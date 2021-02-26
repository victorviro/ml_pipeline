import requests

from src.download_data.domain.data_downloander import IDataDownloander


def download_data(data_downloander: IDataDownloander):
    if isinstance(data_downloander, IDataDownloander):
        data_downloander.download_data()
