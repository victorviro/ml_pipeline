from __future__ import annotations

import os
from typing import Any, Dict

from src.shared.interfaces.data_tracker import IDataTracker
from src.version_data.domain.data_versioner import IDataVersioner


class VersionTrackData:
    """
    Class to version the dataset in some way by calling the method
    `version_data` of object IDataVersioner. It also track information by calling
    the method `track_items` of object IDataTracker.

    :param data_versioner: Object with a method to download data
    :type data_versioner: IDataVersioner
    :param data_tracker: Object with methods to track data into an experiment run
    :type data_tracker: IDataTracker
    """

    def __init__(self, data_versioner: IDataVersioner, data_tracker: IDataTracker):
        self.data_versioner = data_versioner
        self.data_tracker = data_tracker

    def execute(self, data_file_path: str, data_version: float) -> None:
        if not os.path.exists(data_file_path):
            raise FileNotFoundError(
                f'Path of data file does not exist: "{data_file_path}"'
            )
        # Version the dataset (return info to track)
        information_to_log: Dict[str, Any] = self.data_versioner.version_data(
            data_file_path=data_file_path, data_version=data_version
        )
        # Track info in a experiment run
        self.data_tracker.log_information_of_data_versioning(
            information_to_log=information_to_log
        )

    @staticmethod
    def build(
        data_versioner: IDataVersioner, data_tracker: IDataTracker
    ) -> VersionTrackData:
        version_data = VersionTrackData(
            data_versioner=data_versioner, data_tracker=data_tracker
        )
        return version_data
