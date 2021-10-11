import abc
from typing import Any


class IDataVersioner(metaclass=abc.ABCMeta):
    """
    An interface used to version data.
    """

    @abc.abstractmethod
    def version_data(self, data_file_path: Any, data_version: Any) -> Any:
        """
        This method versions a dataset and returns metadata of the versioning.

        :param data_file_path: Path of the data file to be versioned
        :type data_file_path: Any
        :param data_version: Version of the data
        :type data_version: Any
        :return: Metadata of the versioning
        :rtype: Any
        """
        raise NotImplementedError()
