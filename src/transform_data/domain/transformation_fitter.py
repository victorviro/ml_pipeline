import abc
from typing import Any


class ITransformationFitter(metaclass=abc.ABCMeta):
    """
    An interface used to fit a data transformer/preprocesser.
    """

    @abc.abstractmethod
    def fit_transformer(self, dataset: Any) -> Any:
        """
        This method fits a data transformer/preprocesser.

        :param dataset: The dataset to be used when fitting the preprocesser
        :type dataset: Any
        :return: The preprocesser
        :rtype: Any
        """
        raise NotImplementedError()
