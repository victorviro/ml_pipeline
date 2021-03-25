import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from src.download_data.application.download_data_use_case import download_data
from .request_data_downloander import RequestDataDownloander


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_api_url: str
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/download_data")
async def download_data_endpoint(item: Item):

    request_data_downloander = RequestDataDownloander(
        data_api_url=item.data_api_url,
        data_path=item.data_path,
        data_name=item.data_name
    )

    try:
        download_data(request_data_downloander)
        message = 'Data stored and saved succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})

    except Exception as err:
        message = f'Error downloading or storing the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.download_data.infrastructure.request_data_downloander_api:rest_api --port
# 1213
