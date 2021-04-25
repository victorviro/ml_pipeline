import os

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
    """
    def __init__(self, model_server: IModelServer, data_tracker: IDataTracker):
        self.model_server = model_server
        self.data_tracker = data_tracker

    def execute(self, model_file_path: str, version_name: str):
        if not os.path.exists(model_file_path):
            raise Exception('Path of model file does not exist: '
                            f'{model_file_path}')
        # Serve model
        self.model_server.serve_model(
            model_file_path=model_file_path,
            version_name=version_name
        )

    @staticmethod
    def build(model_server: IModelServer, data_tracker: IDataTracker):
        serve_model = ServeModel(model_server=model_server,
                                 data_tracker=data_tracker)
        return serve_model
