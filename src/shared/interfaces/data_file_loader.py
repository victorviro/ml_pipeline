import abc


class IDataFileLoader(metaclass=abc.ABCMeta):
    """
    An interface used to load data from files.
    """

    @abc.abstractmethod
    def load_data(self):
        """
        This method must load data from a file file
        """
        return NotImplementedError
