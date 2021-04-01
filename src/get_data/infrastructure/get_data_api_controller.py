import logging.config

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.shared.logging_config import LOGGING_CONFIG
from .request_data_downloander import RequestDataDownloander
from .json_data_saver import JSONDataSaver
from src.get_data.application.get_data_use_case import GetData


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_api_url: str
    data_path: str
    data_name: str


rest_api = FastAPI()


@rest_api.post("/api/get_data")
async def get_data_endpoint(item: Item):
    data_saver = JSONDataSaver()
    data_downloander = RequestDataDownloander(data_api_url=item.data_api_url)
    file_path = f"{item.data_path}/{item.data_name}.json"

    get_data_use_case = GetData.build(
        data_downloander=data_downloander,
        data_file_saver=data_saver
    )

    try:
        # Download the data and save it
        get_data_use_case.execute(file_path=file_path)
        message = 'Data downloaded and saved succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})

    except Exception as err:
        message = f'Error downloading or storing the dataset: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# uvicorn src.get_data.infrastructure.get_data_api_controller:rest_api --port
# 1213
