import abc
from typing import Any


class IDataFileSaver(metaclass=abc.ABCMeta):
    """
    An interface used to save data to files.
    """

    @abc.abstractmethod
    def save_data(self, file_path: Any, data: Any) -> None:
        """
        This method saves a data file.

        :param file_path: Path where save the data file
        :type file_path: Any
        :param data: Data file to be saved
        :type data: Any
        """
        raise NotImplementedError()
