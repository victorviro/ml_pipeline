from src.serve_model.domain.model_server import IModelServer


def serve_predictions(model_server: IModelServer):
    if isinstance(model_server, IModelServer):
        predictions = model_server.serve_predictions(raw_data)
        return predictions
