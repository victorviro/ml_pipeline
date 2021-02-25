
import logging.config
from src.logging_config import LOGGING_CONFIG

from src.config_variables import (MCPL_DATASET_NAME, MODEL_PATH, ARTIFACT_LOCAL_PATH,
                                  ENDPOINT_PATH, RAW_DATA_PATH, MCPL_SCHEMA)
from src.data.download_raw_data import download_raw_data
from src.data.request_data_downloander import RequestDataDownloander
from src.data_validation.schema_validation import validate_data_schema
from src.data_validation.pandera_schema_validator import PanderaSchemaValidator
from src.models.train_model import data_transformation_and_training
from src.models.model_validation import validate_model
from src.models.hyperparameter_opt import hyper_parameter_search
from src.services import download_data, validate_schema


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")


# # download_raw_data(data_name=MCPL_DATASET_NAME)
# # validate_data_schema(data_name=MCPL_DATASET_NAME)
# artifact_uri = data_transformation_and_training(data_name=MCPL_DATASET_NAME,
#                                                 alpha=0.1, l1_ratio=0.1)
# print(artifact_uri)
# model_path = f'{artifact_uri}/{ARTIFACT_LOCAL_PATH}/model.pkl'
# validate_model(data_name=MCPL_DATASET_NAME, model_path=model_path)
# # hyper_parameter_search(data_name=MCPL_DATASET_NAME)

# DDD
# request_data_downloander = RequestDataDownloander(
#     endpoint_path=ENDPOINT_PATH, data_path=RAW_DATA_PATH, data_name=MCPL_DATASET_NAME
# )
# download_data(data_downloander=request_data_downloander)

pandera_schema_validator = PanderaSchemaValidator(
    schema=MCPL_SCHEMA, data_path=RAW_DATA_PATH, data_name=MCPL_DATASET_NAME
)
validate_schema(pandera_schema_validator)
