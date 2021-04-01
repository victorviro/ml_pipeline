import abc


class IModelValidator(metaclass=abc.ABCMeta):
    """
    An interface used to validate a model.
    """

    @abc.abstractmethod
    def validate_model(self):
        """
        This method must validate the model in some way
        """
