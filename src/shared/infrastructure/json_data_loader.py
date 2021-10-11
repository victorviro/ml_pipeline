import json
import logging

from src.shared.interfaces.data_file_loader import IDataFileLoader

logger = logging.getLogger(__name__)


class JSONDataLoader(IDataFileLoader):
    @staticmethod
    def load_data(file_path: str) -> dict:

        with open(file_path, "r") as output_file:
            data = json.load(output_file)

        msg = f"JSON data loaded succesfully from file in path: {file_path}"
        logger.info(msg)
        return data
