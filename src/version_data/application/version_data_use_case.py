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

    def execute(self, relative_data_file_path: str, data_version: float,
                git_remote_name: str, git_branch_name: str):

        if not os.path.exists(relative_data_file_path):
            raise Exception('Path of data file does not exist: '
                            f'"{relative_data_file_path}"')
        self.data_versioner.version_data(
            relative_data_file_path=relative_data_file_path,
            data_version=data_version,
            git_remote_name=git_remote_name,
            git_branch_name=git_branch_name
        )

    @staticmethod
    def build(data_versioner: IDataVersioner):
        version_data = VersionData(data_versioner=data_versioner)
        return version_data
