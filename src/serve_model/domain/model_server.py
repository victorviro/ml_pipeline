import abc


class IModelServer(metaclass=abc.ABCMeta):
    """
    An interface used to serve a model.
    """

    @abc.abstractmethod
    def serve_model(self, model_path: str, model_version: str):
        """
        This method serves a model to make preditions.

        :param model_path: The path/uri of the model
        :type model_path: str
        :param model_version: The model's version
        :type model_version: str
        """
        raise NotImplementedError()
