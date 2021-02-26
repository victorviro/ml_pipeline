import logging

from fastapi import FastAPI
from pydantic import BaseModel

from src.download_data.application.download_data_use_case import download_data
from .request_data_downloander import RequestDataDownloander


logger = logging.getLogger(__name__)


class Item(BaseModel):
    endpoint_path: str
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/download_data_endpoint")
async def root(item: Item):

    request_data_downloander = RequestDataDownloander(
        endpoint_path=item.endpoint_path,
        data_path=item.data_path,
        data_name=item.data_name
    )

    try:
        download_data(request_data_downloander)
        return {'message': 'succes'}  # 200
    except Exception as err:
        return {'message': str(err)}  # 400

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.download_data.infrastructure.request_data_downloander_api:rest_api --port
# 1213
