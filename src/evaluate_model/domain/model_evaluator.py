import abc
from typing import Any


class IModelEvaluator(metaclass=abc.ABCMeta):
    """
    An interface used to evaluate a model.
    """

    @abc.abstractmethod
    def evaluate_model(self, dataset: Any, model: Any) -> Any:
        """
        This method evaluates a model in a evaluation dataset and return information of
        the evaluation (metrics).

        :param dataset: The dataset used to evaluate the model
        :type dataset: Any
        :param model: The model trained to be evaluated
        :type model: Any
        :return: Information of the model evaluation
        :rtype: Any
        """
        raise NotImplementedError()
