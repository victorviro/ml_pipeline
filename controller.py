
import logging.config
import requests
import json
from src.shared.logging_config import LOGGING_CONFIG
from src.shared.constants import (DATASET_NAME, MODEL_NAME, VERSION,
                                  URL_DATA_MCPL_QUOTES_IMAGE_API, RAW_DATA_PATH,
                                  TRANSFORMED_DATA_PATH, RMSE_THRESOLD, MODELS_PATH,
                                  TRANSFORMER_PIPELINE_NAME, TRANSFORMER_PIPE_PATH)

RAW_DATA_PATH = '/mcpl_prediction/data/01_raw'
TRANSFORMED_DATA_PATH = '/mcpl_prediction/data/04_model_input'
MODELS_PATH = '/mcpl_prediction/models'
TRANSFORMER_PIPE_PATH = '/mcpl_prediction/artifact_store'
MLFLOW_RUN_ID = '9dfa36b182604f548da8b2586b7890ef'
# logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger("controller")

# # Download data
body = {
    'data_api_url': URL_DATA_MCPL_QUOTES_IMAGE_API,
    'data_path': RAW_DATA_PATH,
    'data_name': DATASET_NAME
}
# Request to Fast API to get dataset
url_api = 'http://0.0.0.0:1213/api/get_data'
request = requests.post(url_api, data=json.dumps(body))
request_content = request.content
print(request.content)

# Validate data schema
body = {
    'data_path': RAW_DATA_PATH,
    'data_name': DATASET_NAME
}
# Request to Fast API to validate the shema of the dataset
# url_api = 'http://0.0.0.0:1214/api/validate_data_schema'
url_api = 'http://validate_data:1214/api/validate_data_schema'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)

# # Transform data
# Fit transformer
body = {
    'data_path': RAW_DATA_PATH,
    'data_name': DATASET_NAME,
    'transformer_pipe_path': TRANSFORMER_PIPE_PATH,
    'pipe_name': 'transformer_pipeline',
    'size_test_split': 0.33,
    'test_split_seed': 1,
    'model_name': MODEL_NAME,
    'mlflow_run_id': MLFLOW_RUN_ID
}
# Request to Fast API to transform the data
# url_api = 'http://0.0.0.0:1215/api/fit_transformer_pipeline'
url_api = 'http://transform_data:1215/api/fit_transformer_pipeline'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)
# Transform data
data = {
    "font_size": [66],
    "rows_number": [256],
    "cols_number": [500],
    "char_number_text": [44]
}
body = {
    "data": data,
    'transformer_pipe_path': TRANSFORMER_PIPE_PATH,
    'pipe_name': 'transformer_pipeline'
}
# url_api = 'http://0.0.0.0:1215/api/transform_data'
url_api = 'http://transform_data:1215/api/transform_data'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)

# Train model
body = {
    'raw_data_path': RAW_DATA_PATH,
    'data_name': DATASET_NAME,
    'alpha': 0.1,
    'l1_ratio': 0.1,
    'transformer_name': TRANSFORMER_PIPELINE_NAME,
    'model_name': MODEL_NAME,
    'size_test_split': 0.33,
    'test_split_seed': 1,
    'model_seed': 42,
    'mlflow_run_id': MLFLOW_RUN_ID
}
# Request to Fast API to train the model
# url_api = 'http://0.0.0.0:1216/api/train_model'
url_api = 'http://train_model:1216/api/train_model'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)

# Version data
body = {
    'data_path': RAW_DATA_PATH,
    'data_name': 'data',
    'data_version': 1.5,
    'git_remote_name': 'origin',
    'git_branch_name': 'master',
    'mlflow_run_id': MLFLOW_RUN_ID
}
# Request to Fast API to train the model
# url_api = 'http://0.0.0.0:1217/api/version_data'
url_api = 'http://version_data:1217/api/version_data'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)


# Validate model
body = {
    'raw_data_path': RAW_DATA_PATH,
    'data_name': DATASET_NAME,
    'size_test_split': 0.33,
    'test_split_seed': 1,
    'rmse_threshold': RMSE_THRESOLD,
    'mlflow_run_id': MLFLOW_RUN_ID
}
# Request to Fast API to train the model
# url_api = 'http://0.0.0.0:1218/api/validate_model'
url_api = 'http://validate_model:1218/api/validate_model'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)

# Serve model
body = {
    'font_size': 33,
    'rows_number': 233,
    'cols_number': 344,
    'char_number_text': 44
}
# Request to Fast API to train the model
# url_api = 'http://0.0.0.0:1219/api/served_model'
url_api = 'http://serve_model:1219/api/served_model'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)
