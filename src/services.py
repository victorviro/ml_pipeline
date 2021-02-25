from src.core import IDataDownloander, IDataValidator


def download_data(data_downloander: IDataDownloander):
    if isinstance(data_downloander, IDataDownloander):
        data_downloander.download_data()
