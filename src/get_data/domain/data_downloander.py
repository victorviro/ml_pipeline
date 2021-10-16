import abc
from typing import Any


class IDataDownloander(metaclass=abc.ABCMeta):
    """
    An interface used to download data.
    """

    @abc.abstractmethod
    def download_data(self) -> Any:
        """
        This method downloads data.

        :return: The data downloaded
        :rtype: Any
        """
        raise NotImplementedError()
