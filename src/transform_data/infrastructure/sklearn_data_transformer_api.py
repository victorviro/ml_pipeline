import logging

from fastapi import FastAPI
from fastapi import status  # starlette statuses
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.transform_data.application.transform_data_use_case import transform_data
from.sklearn_data_transformer import SklearnDataTransformer


logger = logging.getLogger(__name__)


class Item(BaseModel):
    data_path: str
    data_name: str
    data_output_path: str


rest_api = FastAPI()


@rest_api.post("/api/transform_data")
async def transform_data_endpoint(item: Item):
    sklearn_data_transformer = SklearnDataTransformer(
        data_path=item.data_path,
        data_name=item.data_name,
        data_output_path=item.data_output_path
    )

    try:
        transform_data(sklearn_data_transformer)
        message = 'Data preprocessed succesfully'
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'message': message})
    except Exception as err:
        message = f'Error preprocessing the data: {str(err)}'
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'message': message})

# cd /home/lenovo/Documents/projects/mcpl_prediction
# source venv/bin/activate
# uvicorn src.transform_data.infrastructure.sklearn_data_transformer_api:rest_api
# --port 1215
