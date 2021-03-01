Max char per line prediction
==============================

## Description

Project to train a model for predicting the max char per line. It includes the full pipeline.

- Data ingestion
- Data validation
- Data versioning
- Data preprocessing/transformation
- Model training
- Model evaluation/validation
- Model versioning
- Model deployment


## Set up

### Via venv
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

### Via docker

See the reference documentation in `docker_README.md`.
```bash
# Build images and up containers
docker-compose up --build -d
# List containers
docker ps
# Stops containers and removes containers
docker-compose down
# See the logs of the container
docker logs mlflow
# Enter into a container
docker exec -it mlflow bash
# List volumes
docker volume ls
# Remove a specific volume
docker volume rm mcpl_prediction_vol_postres1
# Stop postgresql service
sudo service postgresql stop
```

## Steps

The idea is to apply DDD principles. We also create an api through FastAPI per use case (step) in order to separate the code from the pipeline which is defined as an airflow DAG (in `src/airflow_dags`). The structure folder of the project is available in the documentation of the project.

### 1. Data Ingestion

Get the dataset through a request to the REST API of the quotes image project.

**NOTE**: Run the backend of the project quotes image to allow the endpoint works:
```
backend/venv/bin/python3.7 backend/manage.py runserver
```

Debug via `controller.py`. The python code is in `src/download_data/`. A json file (the dataset) is stored in `data/01_raw/`. The name of the dataset is defined in `src/config_variables.py`.

Run the api: 
```bash
uvicorn src.download_data.infrastructure.request_data_downloander_api:rest_api --port 1213
```
### 2. Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline.

Debug via `controller.py`. The code is in `src/validate_data_schema/`.

Run the api: 
```bash
uvicorn src.validate_data_schema.infrastructure.pandera_schema_validator_api:rest_api --port 1214
```

TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).


### 3. Data versioning with DVC

To see the steps as in the first time we run the project, check the reference documentation in `documentation/DVC_data_versioning.md`.

Debug via `controller.py`. The code is in `src/version_data/`.

Run the api: 
```bash
uvicorn src.version_data.infrastructure.dvc_data_versioner_api:rest_api --port 1217
```

TODO: add command to push data versioned in dvc storage.


### 4. Exploratory data analysis (EDA)

Open notebook in `src/notebooks/EDA_MCPL_data.ipynb` (after launch jupyter notbook). To see how to use jupyter notebooks with VScode in this project, see the reference documentation in `documentation/jupyter_notebooks.md`.

```bash
cd Documents/projects/mcpl_prediction
source venv/bin/activate
jupyter notebook
```
**Note**: Recommended to clear outputs of the notebook before save it (to don't commit them).

TODO: up jupyter notebook in a docker container


### 5. Data preprocessing 

Tranform data before training the model using Scikit-learn (standard scaler and custom transformation). A json file (the dataset transformed) is stored in `data/04_model_input/`.

Debug via `controller.py`. The code is in `src/transform_data/`.

Run the api: 
```bash
uvicorn src.transform_data.infrastructure.sklearn_data_transformer_api:rest_api --port 1215
```

### 6. Model training

Train the model using Scikit-learn (regression model) tracking the experiment (metrics, hyperparameters,...) with MLflow (to see how configure a backend db store in MLflow see the reference documentation in `documentation/mlflow_backend_db.md`.). A pickle file (the model trained) is stored in `data/04_model_input/`.

Debug via `controller.py`. The code is in `src/train_model/`.

Run the api: 
```bash
uvicorn src.train_model.infrastructure.mlflow_sklearn_trainer_api:rest_api --port 1216
```

- *Note*: The MLflow ui is available here: http://0.0.0.0:5000 

### 7. Hyperparameter optimization

Optimize hyperparameters using Scikit-learn and hyperopt tracking the experiment (metrics, hyperparameters,...) with MLflow.

Debug via `controller.py`. The code is in `src/optimize_hyperparameters/`.

Run the api: 
```bash

```
TODO: create the api and test it in `controller.py`.

### 8. Model validation

The model is validated if the square root of mean squared error smaller that the thresold fixed (defined in the file `src/config_variables.py`).

Debug/run via `controller.py`. The file to validate the model is `src/models/model_validation.py`.
Debug via `controller.py`. The code is in `src/validate_model/`.

TODO: add some ways to validate the model (for example, if the performace of the new model trained in better than the model currently in production).

### 9. Model versioning

For now, we don't version the model in DVC (it keeps tracked in MLFlow).
