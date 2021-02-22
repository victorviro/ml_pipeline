Max char per line prediction
==============================

## Description

Project to train a model for predicting the max char per line. It includes the full pipeline.
- Data ingestion
- Data validation
- Data versioning
- Data preprocessing/transformation
- Training
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
```

## Steps

### 1. Data Ingestion

Get the dataset through a request to the REST API of the quotes image project.

**NOTE**: Run the backend of the project quotes image to allow the endpoint works:
```
backend/venv/bin/python3.7 backend/manage.py runserver
```

Debug via `controller.py` or run directly with `python controller.py`. The python file to download the dataset is `src/data/download_raw_data.py`. Json data is stored in `data/01_raw/`. The name of the dataset is defined in `src/config_variables.py`

### 2. Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline (building features).

Debug/run via `controller.py` or run directly with `python controller.py`. The file to validate the schema of the dataset is `src/data_validation/schema_validation.py`.


TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).

### 3. Data versioning with DVC

To see the steps as in the first time we run the project, check the reference documentation in `documentation/DVC_data_versioning.md`.

Run `dvc add` again to track the latest version.

```bash
dvc add data/01_raw/data.json
```

Usually we would also run `git commit` and `dvc push` to save the changes:

```bash
# Using the command line
git add data/01_raw/data.json.dvc
git commit -m "Updated raw data (max_char_per_line raw data version X)"
# git push
```

```bash
dvc push
```

### 4. Exploratory data analysis (EDA)

Open notebook in `src/notebooks/EDA_MCPL_data.ipynb` (after launch jupyter notbook). To see how use jupyter notebooks with VScode in this project see the reference documentation in `documentation/jupyter_notebooks.md`.

```bash
cd Documents/projects/mcpl_prediction
source venv/bin/activate
jupyter notebook
```

**Note**: Recommended to clear outputs of the notebook before save it (to don't commit them).

TODO: up jupyter notebook in the mlflow container

### 5. Data preprocessing 

- Added custom transformation for sklearn to use in pipeline (feature engineered `ratio_cols_rows` in `src/features/custom_transformations_sklearn.py`).
- Normalized features in pipeline when training the model.


### 6. Model training

Debug/run via `controller.py` or run directly with `python controller.py`. The file to train the model is `src/models/train_model.py`.


### 7. Model validation

The model is validated if the square root of mean squared error smaller that the thresold fixed (defined in the file `src/config_variables.py`).

Debug/run via `controller.py`. The file to validate the model is `src/models/model_validation.py`.


#### 8. Comparing the models

To see how configure a backend database store in MLflow see the reference documentation in `documentation/mlflow_backend_db.md`.

If docker container is running, the ui is available here: http://0.0.0.0:5000.
If docker is not used, see the reference to launch the ui with the command `mlflow server ...`

### 9. Model versioning

For now, we don't version the model in DVC (it keeps tracked in MLFlow).

### 10. Model deployment

A description of how to deploy a model tracked by MLflow is available in the reference documentation (`documentation/mlflow_deployment.md`).

Open a new window command line and run:

``` bash
cd Documents/projects/mcpl_prediction
source venv/bin/activate
# mlflow models serve -m /home/lenovo/viro/artifact_root/1/5ff27d579438492e9a5bfa59bb5d0a61/artifacts/pipeline -p 1336
#mlflow models serve -m /home/lenovo/Documents/projects/mcpl_prediction/models/artifacts/pipeline -p 1336
mlflow models serve -m ./models/artifacts/pipeline -p 1336
```

Once we have deployed the server (it's running), we can get predictions though a request 

```bash
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["font_size", "rows_number","cols_number", "char_number_text"],"data":[[109, 1291, 730, 46]]}' http://127.0.0.1:1336/invocations
```

### TODO create tag of version v1


