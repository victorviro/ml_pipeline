import abc


class IModelValidator(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate_model') and
                callable(subclass.validate_model))

    @abc.abstractmethod
    def validate_model(self):
        """
        This method must validate the model in some way
        """
