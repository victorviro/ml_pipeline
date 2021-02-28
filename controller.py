
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
# url_api = 'http://127.0.0.1:1213/api/download_data'
# request = requests.post(url_api, data=json.dumps(body))
# request_content = request.content
# # json.loads(request_content.decode('utf-8'))
# print(request.content)

# Validate data schema
# body = {
#     'data_path': RAW_DATA_PATH,
#     'data_name': MCPL_DATASET_NAME
# }
# # Request to Fast API to validate the shema of the dataset
# url_api = 'http://127.0.0.1:1214/api/validate_data_schema'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# # Tranform data
# body = {
#     'data_path': RAW_DATA_PATH,
#     'data_name': MCPL_DATASET_NAME,
#     'data_output_path': TRANSFORMED_DATA_PATH
# }
# # Request to Fast API to transform the data
# url_api = 'http://127.0.0.1:1215/api/transform_data'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Train model
# body = {
#     'raw_data_path': RAW_DATA_PATH,
#     'transformed_data_path': TRANSFORMED_DATA_PATH,
#     'data_name': MCPL_DATASET_NAME,
#     'alpha': 0.1,
#     'l1_ratio': 0.1
# }
# # Request to Fast API to train the model
# url_api = 'http://127.0.0.1:1216/api/train_model'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Version data
body = {
    'relative_data_path': 'data/01_raw',
    'data_name': 'data',
    'data_version': 1,
    'git_remote_name': 'origin',
    'git_branch_name': 'master'
}
# Request to Fast API to train the model
url_api = 'http://127.0.0.1:1217/api/version_data'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)
