import json
import logging

from src.get_data.domain.data_file_saver import IDataFileSaver

logger = logging.getLogger(__name__)


class JSONDataSaver(IDataFileSaver):
    @staticmethod
    def save_data(file_path: str, data: dict):

        with open(file_path, "w") as output_file:
            json.dump(data, output_file, default=str)

        msg = f"Data file stored succesfully in path: {file_path}"
        logger.info(msg)
