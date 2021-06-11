import os
from dotenv import load_dotenv
load_dotenv()


DATASET_NAME = 'data'
DATASET_SCHEMA_FILENAME = 'schema'
VERSION = 1.2
TARGET_VARIABLE_NAME = 'max_char_per_line'

PROJECT_PATH = os.getcwd()
# Data paths
RELATIVE_DATA_PATH = 'data'
RELATIVE_RAW_DATA_PATH = f'{RELATIVE_DATA_PATH}/01_raw'
RAW_DATA_PATH = f'{PROJECT_PATH}/{RELATIVE_RAW_DATA_PATH}'
RELATIVE_TRANSFORMED_DATA_PATH = f'{RELATIVE_DATA_PATH}/04_model_input'
TRANSFORMED_DATA_PATH = f'{PROJECT_PATH}/{RELATIVE_TRANSFORMED_DATA_PATH}'

TRANSFORMER_PIPELINE_NAME = 'transformer_pipeline'

# Model path
RELATIVE_MODELS_PATH = 'models'
MODELS_PATH = f'{PROJECT_PATH}/{RELATIVE_MODELS_PATH}'
TRANSFORMER_PIPE_PATH = f'{PROJECT_PATH}/artifact_store'
MODEL_NAME = 'model'
REGISTRY_MODEL_NAME = 'mcpl'

# Git info
GIT_REMOTE_NAME = 'origin'
GIT_BRANCH_NAME = 'master'

# URL request MCPL data quotes image api http://127.0.0.1:8000/api/v1/max_char_per_l...
URL_DATA_MCPL_QUOTES_IMAGE_API = (f'http://{os.getenv("HOST_QUOTES_IMAGE_API")}:'
                                  f'{os.getenv("PORT_QUOTES_IMAGE_API")}/'
                                  f'{os.getenv("ENDPOINT_DATA_MCPL_QUOTES_IMAGE_API")}/')

# Model training
SIZE_TEST_SPLIT = 0.33
TEST_SPLIT_SEED = 1
TRAIN_MODEL_EXPERIMENT_NAME = 'Model Training'
MODEL_SEED = 42
L1_RATIO_PARAM_MODEL = 0.1
ALPHA_PARAM_MODEL = 0.1

# MLflow
MLFLOW_API_URI = f'{os.getenv("MLFLOW_TRACKING_URI")}/api'
MLFLOW_API_ENDPOINT_LOG_BATCH = '2.0/mlflow/runs/log-batch'
MLFLOW_API_ENDPOINT_GET_RUN = '2.0/mlflow/runs/get'
MLFLOW_API_ENDPOINT_SEARCH_MODEL_VERSIONS = '2.0/preview/mlflow/model-versions/search'
MLFLOW_API_ENDPOINT_UPDATE_MODEL_STAGE = ('2.0/preview/mlflow/model-versions/transition-'
                                          'stage')
MLFLOW_API_ENDPOINT_LATEST_MODEL_VERSION = ('2.0/preview/mlflow/registered-models/get-'
                                            'latest-versions')
MLFLOW_API_ENDPOINT_CREATE_RUN = '2.0/mlflow/runs/create'
MLFLOW_API_ENDPOINT_GET_EXPERIMENT_BY_NAME = '2.0/mlflow/experiments/get-by-name'

# Model validation
RMSE_THRESOLD = 20

# Hyper-parameter optimization
HYPERPARAM_EXPERIMENT_NAME = 'Hyperparameter search'
HYPEROPT_MAX_EVALS = 50


# Urls of use cases APIs
# HOST_USE_CASES_APIS = os.getenv("HOST_USE_CASES_APIS")
URL_GET_DATA_API = (f'http://{os.getenv("HOST_GET_DATA")}:'
                    f'{os.getenv("PORT_GET_DATA")}/'
                    f'{os.getenv("ENDPOINT_GET_DATA")}')

URL_VALIDATE_DATA_API = (f'http://{os.getenv("HOST_VALIDATE_DATA")}:'
                         f'{os.getenv("PORT_VALIDATE_DATA")}/'
                         f'{os.getenv("ENDPOINT_VALIDATE_DATA")}')

URL_FIT_DATA_TRANSFORMER_API = (f'http://{os.getenv("HOST_TRANSFORM_DATA")}:'
                                f'{os.getenv("PORT_TRANSFORM_DATA")}/'
                                f'{os.getenv("ENDPOINT_FIT_DATA_TRANSFORMER")}')

URL_TRAIN_MODEL_API = (f'http://{os.getenv("HOST_TRAIN_MODEL")}:'
                       f'{os.getenv("PORT_TRAIN_MODEL")}/'
                       f'{os.getenv("ENDPOINT_TRAIN_MODEL")}')

URL_VERSION_DATA_API = (f'http://{os.getenv("HOST_VERSION_DATA")}:'
                        f'{os.getenv("PORT_VERSION_DATA")}/'
                        f'{os.getenv("ENDPOINT_VERSION_DATA")}')

URL_VALIDATE_MODEL_API = (f'http://{os.getenv("HOST_VALIDATE_MODEL")}:'
                          f'{os.getenv("PORT_VALIDATE_DATA")}/'
                          f'{os.getenv("ENDPOINT_VALIDATE_DATA")}')


GCP_PROJECT_NAME = 'viroTest'
GCP_BUCKET_NAME = 'mcpl'  # 'mcpl_inference'
GCP_MODEL_NAME_DESTINATION = 'model.pkl'
GCP_REGION = 'europe-west4'
GCP_PROJECT_ID = 'virotest-311212'
GCP_MODEL_NAME = 'mcpl'
GCP_PREDICTION_MACHINE_TYPE = 'n1-standard-2'  # 'n1-standard-4'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    f'{os.getcwd()}/'
    f'{os.getenv("GCP_CREDENTIALS_FILE_REL_PATH")}'
)
