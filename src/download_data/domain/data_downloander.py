import abc


class IDataDownloander(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download_data') and
                callable(subclass.download_data))

    @abc.abstractmethod
    def download_data(self):
        """
        This method must download the data in some way
        """
