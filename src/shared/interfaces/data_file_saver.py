import abc


class IDataFileSaver(metaclass=abc.ABCMeta):
    """
    An interface used to save data to files.
    """

    @abc.abstractmethod
    def save_data(self):
        """
        This method must save data in a file
        """
        return NotImplementedError
