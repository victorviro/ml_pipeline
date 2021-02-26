
import logging.config
import requests
import json
from src.logging_config import LOGGING_CONFIG

from src.config_variables import (MCPL_DATASET_NAME, MODEL_PATH, ARTIFACT_LOCAL_PATH,
                                  ENDPOINT_PATH, RAW_DATA_PATH, MCPL_SCHEMA,
                                  TRANSFORMED_DATA_PATH)


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("controller")

# Download data
body = {
    'endpoint_path': ENDPOINT_PATH,
    'data_path': RAW_DATA_PATH,
    'data_name': MCPL_DATASET_NAME
}
# Request to get dataset
url_api = 'http://127.0.0.1:1213/api/download_data_endpoint'
request = requests.post(url_api, data=json.dumps(body))
print(request.content)
