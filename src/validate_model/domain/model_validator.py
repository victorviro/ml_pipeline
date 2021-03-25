import abc


class IModelValidator(metaclass=abc.ABCMeta):
    """
    An interface used to validate a model.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate_model') and
                callable(subclass.validate_model))

    @abc.abstractmethod
    def validate_model(self):
        """
        This method must validate the model in some way
        """
