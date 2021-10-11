import abc
from typing import Any, Optional


class IModelTrainer(metaclass=abc.ABCMeta):
    """
    An interface used to train a model.
    """

    @abc.abstractmethod
    def train_model(self, dataset: Any, preprocesser: Optional[Any]) -> Any:
        """
        This method trains a model and return training metadata (hyperparameters, model
        etc).

        :param dataset: The dataset used for training the model
        :type dataset: Any
        :param preprocesser: Data preprocesser
        :type preprocesser: Optional[Any]
        :return: Metadata of the training
        :rtype: Any
        """
        raise NotImplementedError()
