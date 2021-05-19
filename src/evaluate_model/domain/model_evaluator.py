import abc


class IModelEvaluator(metaclass=abc.ABCMeta):
    """
    An interface used to evaluate a model.
    """

    @abc.abstractmethod
    def evaluate_model(self):
        """
        This method must evaluate the model in some way
        """
