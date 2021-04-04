import os

from src.version_data.domain.data_versioner import IDataVersioner
from src.shared.interfaces.data_tracker import IDataTracker


class VersionTrackData:
    """
    Class to version the data in some way by calling the method
    `version_data` of object IDataVersioner. It also tracks information of the
    dataset by calling the method `track_data` of object IDataTracker.

    :param data_versioner: Object with a method to download data
    :type data_versioner: IDataVersioner
    :param data_tracker: Object with a method to track data
    :type data_tracker: IDataTracker
    """
    def __init__(self, data_versioner: IDataVersioner, data_tracker: IDataTracker):
        self.data_versioner = data_versioner
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str, data_version: float):

        if not os.path.exists(data_file_path):
            raise Exception('Path of data file does not exist: '
                            f'"{data_file_path}"')
        # Version the dataset (return info to track)
        information_to_track = self.data_versioner.version_data(
            data_file_path=data_file_path,
            data_version=data_version
        )
        # Track information of the dataset
        self.data_tracker.track_data(data=information_to_track)

    @staticmethod
    def build(data_versioner: IDataVersioner, data_tracker: IDataTracker):
        version_data = VersionTrackData(data_versioner=data_versioner,
                                        data_tracker=data_tracker)
        return version_data
