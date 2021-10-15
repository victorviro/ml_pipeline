import abc
from typing import Any


class IModelValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def validate_model(self, metrics: Any, metrics_threshold: Any) -> bool:
        """
        This method validates a model.

        :param metrics: Metrics of the model's
        :type metrics: Any
        :param metrics_threshold: Threshold values of the metrics
        :type metrics_threshold: Any
        :return: If the model is validated
        :rtype: bool
        """
        raise NotImplementedError()
