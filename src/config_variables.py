import os
from dotenv import load_dotenv
import pandera
load_dotenv()


MCPL_DATASET_NAME = 'data'
VERSION = 'v1'

PROJECT_PATH = os.getcwd()
DATA_PATH = f'{PROJECT_PATH}/data'
RAW_DATA_PATH = f'{DATA_PATH}/01_raw'
TRANSFORMED_DATA_PATH = f'{DATA_PATH}/04_model_input'
MODELS_PATH = f'{PROJECT_PATH}/models'
MODEL_NAME = 'model'

# Get endpoint request path to fetch the dataset
ENDPOINT_PATH = f'{os.getenv("ENDPOINT_URL")}{os.getenv("MCPL_ENDPOINT_NAME")}/'

# Model training
MCPL_TEST_SPLIT = 0.33
TEST_SPLIT_SEED = 1
TRAIN_MODEL_EXP_NAME = 'Model Training'
MLFLOW_TRACKING_URI = f'http://{os.getenv("MLFLOW_HOST")}:{os.getenv("MLFLOW_PORT")}'
MODEL_SEED = 42

# Model validation
RMSE_THRESOLD = 20

# Hyper-parameter optimization
HYPER_PARAMETER_EXP_NAME = 'Hyperparameter search'
HYPEROPT_MAX_EVALS = 50


ARTIFACT_LOCAL_PATH = 'model'
ARTIFACTS_URI = ('/home/lenovo/Documents/projects/mcpl_prediction/mlruns/2/ca63e9'
                 f'5ea1f0426c835d94c8f29334e2/artifacts')

# MODEL_PATH = f'{ARTIFACTS_URI}/{ARTIFACT_LOCAL_PATH}/model.pkl'
# MODEL_PATH = './mlruns/0/cba6098fa7bc45bfb0f3eea60fa15a98/artifacts/pipeline/model.pkl'

URL_DOWNLOAD_DATA_API = 'http://127.0.0.1:1213/api/download_data'
URL_VALIDATE_DATA_API = 'http://127.0.0.1:1214/api/validate_data_schema'
URL_TRANSFORM_DATA_API = 'http://127.0.0.1:1215/api/transform_data'
URL_TRAIN_MODEL_API = 'http://127.0.0.1:1216/api/train_model'
URL_VERSION_DATA = 'http://127.0.0.1:1217/api/version_data'
