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
#docker volume rm mcpl_prediction_vol_postres1
#docker volume ls
# sudo service postgresql stop
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

### 2. Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline (building features).

Debug via `controller.py`. The code is in `src/validate_data_schema/`.

TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).
