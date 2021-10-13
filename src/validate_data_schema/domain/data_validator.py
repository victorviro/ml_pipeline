import abc
from typing import Any


class IDataValidator(metaclass=abc.ABCMeta):
    """
    An interface used to validate data.
    """

    @abc.abstractmethod
    def validate_data(self, dataset: Any, dataset_schema_info: Any):
        """
        This method validates the data.

        :param dataset: The dataset to be validated
        :type dataset: Any
        :param dataset_schema_info: Information of the valid schema of the dataset
        :type dataset_schema_info: Any
        """
        raise NotImplementedError()
