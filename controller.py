
import logging.config
import requests
import json
from src.logging_config import LOGGING_CONFIG

from src.config_variables import (MCPL_DATASET_NAME, MODEL_PATH, ARTIFACT_LOCAL_PATH,
                                  ENDPOINT_PATH, RAW_DATA_PATH,
                                  TRANSFORMED_DATA_PATH)


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")

# # Download data
# body = {
#     'endpoint_path': ENDPOINT_PATH,
#     'data_path': RAW_DATA_PATH,
#     'data_name': MCPL_DATASET_NAME
# }
# # Request to Fast API to get dataset
# url_api = 'http://127.0.0.1:1213/api/download_data_endpoint'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Validate data schema
# body = {
#     'data_path': RAW_DATA_PATH,
#     'data_name': MCPL_DATASET_NAME
# }
# # Request to Fast API to validate the shema of the dataset
# url_api = 'http://127.0.0.1:1214/api/validate_data_schema_endpoint'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Tranform data
body = {
    'data_path': RAW_DATA_PATH,
    'data_name': MCPL_DATASET_NAME,
    'data_output_path': TRANSFORMED_DATA_PATH
}
# Request to Fast API to validate the shema of the dataset
url_api = 'http://127.0.0.1:1215/api/transform_data'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)
