import os

from dotenv import load_dotenv

load_dotenv()


DATASET_NAME = "data"
DATASET_SCHEMA_FILENAME = "schema"
VERSION = 1.2
TARGET_VARIABLE_NAME = "max_char_per_line"

PROJECT_PATH = os.getcwd()
# Data paths
RELATIVE_DATA_PATH = "data"
RELATIVE_RAW_DATA_PATH = f"{RELATIVE_DATA_PATH}/01_raw"
RAW_DATA_PATH = f"{PROJECT_PATH}/{RELATIVE_RAW_DATA_PATH}"


TRANSFORMER_PIPELINE_NAME = "transformer_pipeline"
MODEL_NAME = "model"
REGISTRY_MODEL_NAME = "mcpl"

# Git info
GIT_REMOTE_NAME = "origin"
GIT_BRANCH_NAME = "master"

# URL request MCPL data quotes image api http://127.0.0.1:8000/api/v1/max_char_per_l...
URL_DATA_MCPL_QUOTES_IMAGE_API = (
    f'http://{os.getenv("HOST_QUOTES_IMAGE_API")}:'
    f'{os.getenv("PORT_QUOTES_IMAGE_API")}/'
    f'{os.getenv("ENDPOINT_DATA_MCPL_QUOTES_IMAGE_API")}/'
)

# Model training
SIZE_TEST_SPLIT = 0.33
TEST_SPLIT_SEED = 1
TRAIN_MODEL_EXPERIMENT_NAME = "Model Training"
MODEL_SEED = 42
L1_RATIO_PARAM_MODEL = 0.1
ALPHA_PARAM_MODEL = 0.1

# Model validation
RMSE_THRESOLD = 20

# Urls of use cases APIs
# HOST_USE_CASES_APIS = os.getenv("HOST_USE_CASES_APIS")
URL_GET_DATA_API = (
    f'http://{os.getenv("HOST_GET_DATA")}:'
    f'{os.getenv("PORT_GET_DATA")}/'
    f'{os.getenv("ENDPOINT_GET_DATA")}'
)

URL_VALIDATE_DATA_API = (
    f'http://{os.getenv("HOST_VALIDATE_DATA")}:'
    f'{os.getenv("PORT_VALIDATE_DATA")}/'
    f'{os.getenv("ENDPOINT_VALIDATE_DATA")}'
)

URL_FIT_DATA_TRANSFORMER_API = (
    f'http://{os.getenv("HOST_TRANSFORM_DATA")}:'
    f'{os.getenv("PORT_TRANSFORM_DATA")}/'
    f'{os.getenv("ENDPOINT_FIT_DATA_TRANSFORMER")}'
)

URL_TRAIN_MODEL_API = (
    f'http://{os.getenv("HOST_TRAIN_MODEL")}:'
    f'{os.getenv("PORT_TRAIN_MODEL")}/'
    f'{os.getenv("ENDPOINT_TRAIN_MODEL")}'
)

URL_VERSION_DATA_API = (
    f'http://{os.getenv("HOST_VERSION_DATA")}:'
    f'{os.getenv("PORT_VERSION_DATA")}/'
    f'{os.getenv("ENDPOINT_VERSION_DATA")}'
)

URL_EVALUATE_MODEL_API = (
    f'http://{os.getenv("HOST_EVALUATE_MODEL")}:'
    f'{os.getenv("PORT_EVALUATE_MODEL")}/'
    f'{os.getenv("ENDPOINT_EVALUATE_MODEL")}'
)

URL_VALIDATE_MODEL_API = (
    f'http://{os.getenv("HOST_VALIDATE_MODEL")}:'
    f'{os.getenv("PORT_VALIDATE_MODEL")}/'
    f'{os.getenv("ENDPOINT_VALIDATE_MODEL")}'
)


GCP_REGION = "europe-west4"
GCP_MODEL_NAME = "mcpl"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    f"{os.getcwd()}/" f'{os.getenv("GCP_CREDENTIALS_FILE_REL_PATH")}'
)
