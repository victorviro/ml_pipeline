import os

PROJECT_PATH = os.getcwd()
DATA_PATH = f'{PROJECT_PATH}/data'
RAW_DATA_PATH = f'{DATA_PATH}/01_raw'


# Endpoints
ENDPOINT_URL = 'http://127.0.0.1:8000/api/v1/'
MCPL_ENDPOINT_NAME = 'max_char_per_line_train_data'

# Get training data
MCPL_TEST_SPLIT = 0.33
MCPL_DATASET_NAME = 'Data_test'
EXPERIMENT_ID = 0
