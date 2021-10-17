import abc
from enum import Enum


class ModelStage(Enum):
    UNDEFINED = "UNDEFINED"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"


class IModelRegister(metaclass=abc.ABCMeta):
    """
    An interface used to interact with Model Registry.
    """

    @abc.abstractmethod
    def register_model(self, name: str) -> None:
        """
        Register the model in Model registry.

        :param name: Name of the registered model
        :type name: str
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def transition_model_version_stage(self, name: str, stage: str) -> None:
        """
        Update model version stage in Model Registry.

        :param name: Name of the registered model
        :type name: str
        :param stage: New desired stage for this model version
        :type stage: str
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_stage_from_enum(self, stage: ModelStage) -> str:
        raise NotImplementedError()
