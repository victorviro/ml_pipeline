import abc
from typing import Any


class IDataTracker(metaclass=abc.ABCMeta):
    """
    An interface used to track data in an experiment.
    """

    @abc.abstractmethod
    def track_metrics(self, metrics: Any) -> None:
        """
        This method track metric values to an experiment.

        :param metrics: The metrics to track
        :type metrics: dict
        """
        raise NotImplementedError()
