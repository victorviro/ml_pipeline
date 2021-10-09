import logging
import pickle

from src.shared.interfaces.data_file_loader import IDataFileLoader

logger = logging.getLogger(__name__)


class PickleDataLoader(IDataFileLoader):
    """
    A class which implements the interface IDataFileLoader to load data from files.
    It loads pickle data.
    """

    @staticmethod
    def load_data(file_path: str):
        """
        Load pickle data from a file.
        """

        with open(file_path, "rb") as file:
            data = pickle.load(file)

        msg = f"Pickle data file loaded succesfully from file in path: {file_path}"
        logger.info(msg)
        return data
