import abc
from typing import Any, Dict


class IDataTracker(metaclass=abc.ABCMeta):
    """
    Interact with an experiment tracking tool (log information, load it, etc).
    """

    @abc.abstractmethod
    def log_information_of_data_versioning(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        """
        Log information of the data versioining (data path in cloud storage, etc).

        :param information_to_log: The information to log
        :type information_to_log: Dict[str, Any]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def log_information_of_data_preprocessor_fitting(
        self, data_preprocessor: Any
    ) -> None:
        """
        Log information of the data preprocessor fitting (preprocessing steps, etc).

        :param data_preprocessor: The data preprocessor fitted
        :type data_preprocessor: Any
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def log_information_of_model_training(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        """
        Log information of the model training (hyperparameters, etc).

        :param information_to_log: The information to log
        :type information_to_log: Dict[str, Any]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def log_information_of_model_evaluation(
        self, information_to_log: Dict[str, Any]
    ) -> None:
        """
        Log information of the model evaluation (performance metrics, etc).

        :param information_to_log: The information to log
        :type information_to_log: Dict[str, Any]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_information_logged_for_model_validation(self) -> Dict[str, Any]:
        """
        Get information logged for model validation (performance metrics, etc).

        :return: The information logged to get
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load_model_logged(self) -> Any:
        """
        Load model fitted logged.

        :return: The model
        :rtype: Any
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def load_data_preprocessor_logged(self) -> Any:
        """
        Load data preprocessor fitted logged.

        :return: The model
        :rtype: Any
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_model_path_in_storage(self) -> str:
        """
        Get the path of the model in the storage.

        :return: Path of the model.
        :rtype: str
        """
        raise NotImplementedError()
