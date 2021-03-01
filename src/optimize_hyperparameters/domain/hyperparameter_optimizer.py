import abc


class IHyperparameterOptimizer(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'optimize_hyperparameters') and
                callable(subclass.optimize_hyperparameters))

    @abc.abstractmethod
    def optimize_hyperparameters(self):
        """
        This method must train a model optimizing hyperparameters in some way
        """
