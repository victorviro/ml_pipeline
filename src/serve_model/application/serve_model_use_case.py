import os

from src.serve_model.domain.model_server import IModelServer
from src.shared.interfaces.data_tracker import IDataTracker
from src.shared.interfaces.data_file_loader import IDataFileLoader


class ServeModel:
    """
    Class to serve the model in some way by calling the method
    `serve_predictions` of object IModelServer.

    :param model_server: Object with a method to serve the model
    :type model_server: IModelServer
    :param model_file_loader: Object with a method to load model file
    :type model_file_loader: IDataFileLoader
    :param data_tracker: Object with methods to track information
    :type data_tracker: IDataTracker
    """
    def __init__(self, model_server: IModelServer, model_file_loader: IDataFileLoader,
                 data_tracker: IDataTracker):
        self.model_server = model_server
        self.model_file_loader = model_file_loader
        self.data_tracker = data_tracker

    def execute(self, data):

        # Make predictions
        predictions = self.model_server.serve_predictions(
            data=data,
            data_tracker=self.data_tracker,
            model_file_loader=self.model_file_loader
        )
        return predictions

    @staticmethod
    def build(model_server: IModelServer, model_file_loader: IDataFileLoader,
              data_tracker: IDataTracker):
        serve_model = ServeModel(model_server=model_server,
                                 model_file_loader=model_file_loader,
                                 data_tracker=data_tracker)
        return serve_model
