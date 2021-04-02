import os

from src.version_data.domain.data_versioner import IDataVersioner


class VersionData:
    """
    Class to version the data in some way by calling the method
    `version_data` of object IDataVersioner.

    :param data_versioner: Object with a method to download data
    :type data_versioner: IDataVersioner
    """
    def __init__(self, data_versioner: IDataVersioner):
        self.data_versioner = data_versioner

    def execute(self, data_file_path: str, data_version: float):

        if not os.path.exists(data_file_path):
            raise Exception('Path of data file does not exist: '
                            f'"{data_file_path}"')
        self.data_versioner.version_data(
            data_file_path=data_file_path,
            data_version=data_version
        )

    @staticmethod
    def build(data_versioner: IDataVersioner):
        version_data = VersionData(data_versioner=data_versioner)
        return version_data
