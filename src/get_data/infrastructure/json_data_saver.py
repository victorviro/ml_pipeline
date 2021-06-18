import json
import logging

from src.get_data.domain.data_file_saver import IDataFileSaver


logger = logging.getLogger(__name__)


class JSONDataSaver(IDataFileSaver):
    """
    A class which implements the interface IDataFileSaver to save data to a file.
    It saves JSON data.
    """

    def save_data(self, file_path: str, data: dict):
        """
        Save the data.
        """

        with open(file_path, 'w') as output_file:
            json.dump(data, output_file, default=str)

        msg = f'Data stored succesfully in path: {file_path}'
        logger.info(msg)
