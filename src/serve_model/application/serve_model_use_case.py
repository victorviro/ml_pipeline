import os

from src.serve_model.domain.model_server import IModelServer


class ServeModel:
    """
    Class to serve the model in some way by calling the method
    `serve_predictions` of object IModelServer.

    :param model_server: Object with a method to serve the model
    :type model_server: IModelServer
    """
    def __init__(self, model_server: IModelServer):
        self.model_server = model_server

    def execute(self, data):

        # Make predictions
        predictions = self.model_server.serve_predictions(data=data)
        return predictions

    @staticmethod
    def build(model_server: IModelServer):
        serve_model = ServeModel(model_server=model_server)
        return serve_model
