import abc


class IDataDownloander(metaclass=abc.ABCMeta):
    """
    An interface used to download data.
    """

    @abc.abstractmethod
    def download_data(self):
        """
        This method must download the data in some way
        """
        return NotImplementedError
