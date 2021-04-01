import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.serve_model.application.serve_model_use_case import ServeModel
from .sklearn_model_server import SklearnModelServer


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    font_size: int
    rows_number: int
    cols_number: int
    char_number_text: int


rest_api = FastAPI()


@rest_api.post("/api/served_model")
async def serve_model_endpoint(item: Item):
    data = {
        'font_size': [item.font_size],
        'rows_number': [item.rows_number],
        'cols_number': [item.cols_number],
        'char_number_text': [item.char_number_text]
    }
    sklearn_model_server = SklearnModelServer()

    serve_model_use_case = ServeModel.build(model_server=sklearn_model_server)

    try:
        predictions = serve_model_use_case.execute(data=data)
        message = 'Prediction made by the model succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message, 'prediction': predictions[0]})
    except Exception as err:
        message = f'Error making predictions: {str(err)}'
        logger.error(message)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.serve_model.infrastructure.serve_model_api_controller:rest_api --port 1219
