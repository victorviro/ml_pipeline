import os
from dotenv import load_dotenv
import pandera
load_dotenv()


MCPL_DATASET_NAME = 'data2'
VERSION = 'v1'

PROJECT_PATH = os.getcwd()
DATA_PATH = f'{PROJECT_PATH}/data'
RAW_DATA_PATH = f'{DATA_PATH}/01_raw'

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


ARTIFACT_LOCAL_PATH = 'pipeline'
ARTIFACTS_URI = ('/home/lenovo/Documents/projects/mcpl_prediction/mlruns/2/ca63e9'
                 f'5ea1f0426c835d94c8f29334e2/artifacts')

MODEL_PATH = f'{ARTIFACTS_URI}/{ARTIFACT_LOCAL_PATH}/model.pkl'
# MODEL_PATH = './mlruns/0/cba6098fa7bc45bfb0f3eea60fa15a98/artifacts/pipeline/model.pkl'

# Define the schema of the dataset
MCPL_SCHEMA = pandera.DataFrameSchema({
    "max_char_per_line": pandera.Column(int,
                                        checks=pandera.Check.less_than_or_equal_to(100)),
    "font_size": pandera.Column(int, checks=pandera.Check.less_than(1000)),
    "rows_number": pandera.Column(int),
    "cols_number": pandera.Column(int),
    "char_number_text": pandera.Column(int)
})