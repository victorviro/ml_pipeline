import abc


class IDataDownloander(metaclass=abc.ABCMeta):
    """
    An interface used to download data.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download_data') and
                callable(subclass.download_data))

    @abc.abstractmethod
    def download_data(self):
        """
        This method must download the data in some way
        """
