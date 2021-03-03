import os
from dotenv import load_dotenv
load_dotenv()


DATASET_NAME = 'data'
VERSION = '1'


PROJECT_PATH = os.getcwd()
# Data paths
RELATIVE_DATA_PATH = 'data'
RELATIVE_RAW_DATA_PATH = f'{RELATIVE_DATA_PATH}/01_raw'
RAW_DATA_PATH = f'{PROJECT_PATH}/{RELATIVE_RAW_DATA_PATH}'
RELATIVE_TRANSFORMED_DATA_PATH = f'{RELATIVE_DATA_PATH}/04_model_input'
TRANSFORMED_DATA_PATH = f'{PROJECT_PATH}/{RELATIVE_TRANSFORMED_DATA_PATH}'

# Model path
RELATIVE_MODELS_PATH = 'models'
MODELS_PATH = f'{PROJECT_PATH}/{RELATIVE_MODELS_PATH}'
MODEL_NAME = 'model'

# Git info
GIT_REMOTE_NAME = 'origin'
GIT_BRANCH_NAME = 'master'

# URL request MCPL data quotes image api http://127.0.0.1:8000/api/v1/max_char_per_l...
URL_DATA_MCPL_QUOTES_IMAGE_API = (f'http://{os.getenv("HOST_QUOTES_IMAGE_API")}:'
                                  f'{os.getenv("PORT_QUOTES_IMAGE_API")}/'
                                  f'{os.getenv("ENDPOINT_DATA_MCPL_QUOTES_IMAGE_API")}')

# Model training
SIZE_TEST_SPLIT = 0.33
TEST_SPLIT_SEED = 1
TRAIN_MODEL_EXPERIMENT_NAME = 'Model Training'
MLFLOW_TRACKING_URI = f'http://{os.getenv("MLFLOW_HOST")}:{os.getenv("MLFLOW_PORT")}'
MODEL_SEED = 42

# Model validation
RMSE_THRESOLD = 20

# Hyper-parameter optimization
HYPERPARAM_EXPERIMENT_NAME = 'Hyperparameter search'
HYPEROPT_MAX_EVALS = 50


# Urls of use cases APIs
HOST_USE_CASES_APIS = os.getenv("HOST_USE_CASES_APIS")
URL_DOWNLOAD_DATA_API = (f'http://{HOST_USE_CASES_APIS}:'
                         f'{os.getenv("PORT_DOWNLOAD_DATA")}/'
                         f'{os.getenv("ENDPOINT_DOWNLOAD_DATA")}')

URL_VALIDATE_DATA_API = (f'http://{HOST_USE_CASES_APIS}:'
                         f'{os.getenv("PORT_VALIDATE_DATA")}/'
                         f'{os.getenv("ENDPOINT_VALIDATE_DATA")}')

URL_TRANSFORM_DATA_API = (f'http://{HOST_USE_CASES_APIS}:'
                          f'{os.getenv("PORT_TRANSFORM_DATA")}/'
                          f'{os.getenv("ENDPOINT_TRANSFORM_DATA")}')

URL_TRAIN_MODEL_API = (f'http://{HOST_USE_CASES_APIS}:'
                       f'{os.getenv("PORT_TRAIN_MODEL")}/'
                       f'{os.getenv("ENDPOINT_TRAIN_MODEL")}')

URL_VERSION_DATA_API = (f'http://{HOST_USE_CASES_APIS}:'
                        f'{os.getenv("PORT_VERSION_DATA")}/'
                        f'{os.getenv("ENDPOINT_VERSION_DATA")}')

URL_VALIDATE_MODEL_API = (f'http://{HOST_USE_CASES_APIS}:'
                          f'{os.getenv("PORT_VALIDATE_DATA")}/'
                          f'{os.getenv("ENDPOINT_VALIDATE_DATA")}')
