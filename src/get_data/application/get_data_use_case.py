import os

from src.get_data.domain.data_downloander import IDataDownloander
from src.shared.interfaces.data_file_saver import IDataFileSaver


class GetData:
    """
    Class to download the data in some way by calling the method
    `download_data` of object IDataDownloander and store it by calling
    the method `save_data` of object IDataFileSaver

    :param data_downloander: Object with a method to download data
    :type data_downloander: IDataDownloander
    :param data_file_saver: Object with a method to save data
    :type data_file_saver: IDataFileSaver
    """
    def __init__(self, data_downloander: IDataDownloander,
                 data_file_saver: IDataFileSaver):
        self.data_downloander = data_downloander
        self.data_file_saver = data_file_saver

    def execute(self, file_path: str, data_api_url: str):
        # ping
        data: dict = self.data_downloander.download_data(data_api_url=data_api_url)
        if not isinstance(data, dict):
            raise Exception(f'Data downloaded is not a dict. It is a {type(data)}')
        if not os.path.exists(os.path.dirname(file_path)):
            raise Exception(f'Path {os.path.dirname(file_path)} does not exist')
        self.data_file_saver.save_data(file_path=file_path, data=data)

    @staticmethod
    def build(data_downloander: IDataDownloander,
              data_file_saver: IDataFileSaver):

        get_data = GetData(
            data_downloander=data_downloander,
            data_file_saver=data_file_saver
        )
        return get_data
