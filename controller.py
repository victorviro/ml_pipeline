
import logging.config
import requests
import json
from src.logging_config import LOGGING_CONFIG
from src.config_variables import (DATASET_NAME, MODEL_NAME, VERSION,
                                  URL_DATA_MCPL_QUOTES_IMAGE_API, RAW_DATA_PATH,
                                  TRANSFORMED_DATA_PATH, RMSE_THRESOLD, MODELS_PATH)

RAW_DATA_PATH = '/mcpl_prediction/data/01_raw'
TRANSFORMED_DATA_PATH = '/mcpl_prediction/data/04_model_input'
# logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger("controller")

# # Download data
# from src.download_data.application.download_data_use_case import download_data
# from src.download_data.infrastructure.request_data_downloander import RequestDataDownloander
# request_data_downloander = RequestDataDownloander(
#         url_quotes_image_api_mcpl_data=URL_DATA_MCPL_QUOTES_IMAGE_API,
#         data_path=RAW_DATA_PATH,
#         data_name=DATASET_NAME
#     )
# download_data(request_data_downloander)

# body = {
#     'url_quotes_image_api_mcpl_data': URL_DATA_MCPL_QUOTES_IMAGE_API,
#     'data_path': RAW_DATA_PATH,
#     'data_name': DATASET_NAME
# }
# # Request to Fast API to get dataset
# url_api = 'http://0.0.0.1:1213/api/download_data'
# request = requests.post(url_api, data=json.dumps(body))
# request_content = request.content
# # json.loads(request_content.decode('utf-8'))
# print(request.content)

# Validate data schema
# RAW_DATA_PATH = '/mcpl_prediction/data/01_raw'
# body = {
#     'data_path': RAW_DATA_PATH,
#     'data_name': DATASET_NAME
# }
# # Request to Fast API to validate the shema of the dataset
# url_api = 'http://0.0.0.0:1214/api/validate_data_schema'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# # Tranform data
# body = {
#     'data_path': RAW_DATA_PATH,
#     'data_name': DATASET_NAME,
#     'data_output_path': TRANSFORMED_DATA_PATH
# }
# # Request to Fast API to transform the data
# url_api = 'http://0.0.0.0:1215/api/transform_data'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Train model
# body = {
#     'raw_data_path': RAW_DATA_PATH,
#     'transformed_data_path': TRANSFORMED_DATA_PATH,
#     'data_name': DATASET_NAME,
#     'alpha': 0.1,
#     'l1_ratio': 0.1,
#     'version': 1,
#     'model_path': MODELS_PATH,
#     'model_name': MODEL_NAME,
#     'size_test_split': 0.33,
#     'test_split_seed': 1,
#     'model_seed': 42
# }
# # Request to Fast API to train the model
# url_api = 'http://127.0.0.1:1216/api/train_model'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)

# Version data
body = {
    'relative_data_path': 'data/01_raw',
    'data_name': 'data',
    'data_version': VERSION,
    'git_remote_name': 'origin',
    'git_branch_name': 'master'
}
# Request to Fast API to train the model
url_api = 'http://0.0.0.0:1217/api/version_data'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)


# Validate model
# body = {
#     'transformed_data_path': TRANSFORMED_DATA_PATH,
#     'data_name': DATASET_NAME,
#     'model_path': MODELS_PATH,
#     'model_name': MODEL_NAME,
#     'size_test_split': 0.33,
#     'test_split_seed': 1,
#     'rmse_threshold': RMSE_THRESOLD
# }
# # Request to Fast API to train the model
# url_api = 'http://127.0.0.1:1218/api/validate_model'
# request = requests.post(url_api, data=json.dumps(body))
# print(request.content)
