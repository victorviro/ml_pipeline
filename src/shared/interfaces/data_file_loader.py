import abc
from typing import Any


class IDataFileLoader(metaclass=abc.ABCMeta):
    """
    An interface used to load data from files.
    """

    @abc.abstractmethod
    def load_data(self, file_path: Any) -> Any:
        """
        This method loads data from a file.

        :param file_path: The path of the data file
        :type file_path: Any
        :return: The data
        :rtype: Any
        """
        raise NotImplementedError()
