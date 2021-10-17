from src.serve_model.domain.model_server import IModelServer
from src.shared.interfaces.data_tracker import IDataTracker


class ServeModel:
    """
    Class to serve the model in some way by calling the method
    `serve_model` of object IModelServer.

    :param model_server: Object with a method to serve the model
    :type model_server: IModelServer
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    :param model_version: The version numer of the model
    :type model_version: float
    """

    def __init__(
        self,
        model_server: IModelServer,
        data_tracker: IDataTracker,
        model_version: float,
    ):
        self.model_server = model_server
        self.data_tracker = data_tracker
        self.model_version = model_version

    def execute(self):
        # Get path of the model tracked
        model_path = self.data_tracker.get_model_path_in_storage()
        # Serve model
        self.model_server.serve_model(
            model_path=model_path, model_version=self.model_version
        )

    @staticmethod
    def build(
        model_server: IModelServer, data_tracker: IDataTracker, model_version: float
    ):
        serve_model = ServeModel(
            model_server=model_server,
            data_tracker=data_tracker,
            model_version=model_version,
        )
        return serve_model
