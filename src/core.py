import abc


class IDataDownloander(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'download_data') and
                callable(subclass.download_data) and
                hasattr(subclass, 'save_data') and
                callable(subclass.save_data))

    @abc.abstractmethod
    def download_data(self):
        """
        This method must download the data in some way
        """
    @abc.abstractmethod
    def save_data(self):
        """
        This method must save the data in some way
        """
