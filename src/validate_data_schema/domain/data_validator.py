import abc


class IDataValidator(metaclass=abc.ABCMeta):
    """
    An interface used to validate data.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate_data') and
                callable(subclass.validate_data))

    @abc.abstractmethod
    def validate_data(self):
        """
        This method must validate the data in some way
        """
