import abc


class IModelServer(metaclass=abc.ABCMeta):
    """
    An interface used to serve a model.
    """

    @abc.abstractmethod
    def serve_model(self):
        """
        This method must serve a model to make preditions.
        """
