import abc


class IDataValidator(metaclass=abc.ABCMeta):
    """
    An interface used to validate data.
    """

    @abc.abstractmethod
    def validate_data(self):
        """
        This method must validate the data in some way
        """
