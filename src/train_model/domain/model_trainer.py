import abc


class IModelTrainer(metaclass=abc.ABCMeta):
    """
    An interface used to train a model.
    """

    @abc.abstractmethod
    def train_model(self):
        """
        This method must train a model
        """
