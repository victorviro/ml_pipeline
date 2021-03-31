import pickle
import logging

from src.shared.interfaces.data_file_saver import IDataFileSaver


logger = logging.getLogger(__name__)


class PickleDataSaver(IDataFileSaver):
    """
    A class which implements the interface IDataFileSaver to save data to files.
    It saves pickle data.
    """

    def save_data(self, file_path: str, file):
        """
        Save data to a pickle file.
        """

        with open(file_path, 'wb') as f:
            pickle.dump(file, f)

        msg = f'Pickle data file saved succesfully. File in path: {file_path}'
        logger.info(msg)
