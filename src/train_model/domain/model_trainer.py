import abc


class IModelTrainer(metaclass=abc.ABCMeta):
    """
    An interface used to train a model.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'train_model') and
                callable(subclass.train_model))

    @abc.abstractmethod
    def train_model(self):
        """
        This method must train a model
        """
