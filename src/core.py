import abc


class IDataDownloander(metaclass=abc.ABCMeta):
    # def __init__(self):

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


class IDataValidator(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate_data') and
                callable(subclass.validate_data) and
                hasattr(subclass, 'get_data') and
                callable(subclass.get_data))

    @abc.abstractmethod
    def validate_data(self):
        """
        This method must validate the data in some way
        """
    @abc.abstractmethod
    def get_data(self):
        """
        This method must get the data in some way
        """


class IDataTransformer(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'transform_data') and
                callable(subclass.transform_data) and
                hasattr(subclass, 'get_data') and
                callable(subclass.get_data) and
                hasattr(subclass, 'save_data') and
                callable(subclass.save_data))

    @abc.abstractmethod
    def transform_data(self):
        """
        This method must transform the data in some way
        """
    @abc.abstractmethod
    def get_data(self):
        """
        This method must get the data in some way
        """
    @abc.abstractmethod
    def save_data(self):
        """
        This method must save the data in some way
        """
