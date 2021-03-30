import abc


class IDataVersioner(metaclass=abc.ABCMeta):
    """
    An interface used to version data.
    """

    @abc.abstractmethod
    def version_data(self):
        """
        This method must version the data in some way
        """
