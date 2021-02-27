import abc


class IModelTrainer(metaclass=abc.ABCMeta):
    def __init__(self):
        self.data = self.get_data()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'train_model') and
                callable(subclass.train_model))

    @abc.abstractmethod
    def train_model(self):
        """
        This method must train a model
        """
