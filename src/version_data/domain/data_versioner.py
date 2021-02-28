import abc


class IDataVersioner(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'version_data') and
                callable(subclass.version_data))

    @abc.abstractmethod
    def version_data(self):
        """
        This method must version the data in some way
        """
