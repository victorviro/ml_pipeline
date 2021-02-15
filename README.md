Max char per line prediction
==============================

## Description

Project to train a model for predicting the max char per line. It includes the full pipeline.
- Data ingestion
- Data versioning
- Data validation
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

See the refrence documentation in `docker_README.md`.
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
```

## Steps

**NOTE**: In order to run this steps in the pipeline in a airflow DAG we use python functions.

### Get training data / Data Ingestion

Get the dataset through a request to the REST API of the quotes image project.

**NOTE**: Run the backend of the project quotes image to allow the endpoint works:
```
backend/venv/bin/python3.7 backend/manage.py runserver
```

Debug via `controller.py` or run directly with `python controller.py`. The python file to download the dataset is `src/data/download_raw_data.py`. Json data is stored in `data/01_raw/`. The name of the dataset is defined in `src/config_variables.py`

### Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline (building features).

Debug/run via `controller.py`. The file to validate the schema of the dataset is `src/data_validation/schema_validation.py`.


TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).

### DVC versioning the data

To see the steps as in the first time we run the project, in the reference documentation in `references/DVC_data_versioning.md`.

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

### Notebooks (EDA dataset)

Open notebook in `src/notebooks/EDA_MCPL_data.ipynb`. To see how use jupyter notebooks with VScode in this project see the reference documentation in `references/jupyter_notebooks.md`.

**Note**: Recommended to clear outputs of the notebook before save it (to don't commit them).


### Preprocessing the data

- Added custom transformation for sklearn to use in pipeline (feture engineered `ratio_cols_rows` in `src/features/custom_transformations_sklearn.py`).
- Normalized features in pipeline when training the model.


### Train the model

Debug/run via `controller.py`. The file to train the model is `src/models/train_model.py`.

```
python src/models/train_model.py
```

### Model validation

The model is validated if the square root of mean squared error smaller that the thresold fixed (defined in the file `src/config_variables.py`).

Debug/run via `controller.py`. The file to validate the model is `src/models/model_validation.py`.


#### Comparing the models

To see how configure a backend database store in MLflow see the reference documentation in `references/mlflow_backend_db.md`.

Launch the mlflow ui
```bash
mlflow server --backend-store-uri postgresql://mlflow_user:mlflow@localhost/mcpl_mlflow_db \
        --default-artifact-root file:/home/lenovo/viro/artifact_root \
        --host 0.0.0.0 \
        --port 1214
```

Now the Tracking server should be available at the following URL: http://0.0.0.0:1213.

We can set the tracking URI at the beginning of our program, with the same `host:port` as we used to configure the mlflow server (`mlflow.set_tracking_uri('http://0.0.0.0:1213')`) or we can do it with the CLI setting the following environmental variable:

```bash
export MLFLOW_TRACKING_URI='http://0.0.0.0:1213'
```

### Model versioning

The file to train the model outputs the artifact uri (`.../artifacts`). Once the model is validated, we track this directory with DVC. We first copy the artifact dir to `models/`:

```bash
cp -R /home/lenovo/viro/artifact_root/1/5ff27d579438492e9a5bfa59bb5d0a61/artifacts /home/lenovo/Documents/projects/MCPL_prediction/models/
dvc add /home/lenovo/Documents/projects/MCPL_prediction/models/artifacts
```

Usually we would also run `git commit` and `dvc push`.


### Model deployment

A description of how to deploy a model tracked by MLflow is available in the reference documentation (`references/mlflow_deployment.md`).

Open a new window command line and run:

``` bash
cd Documents/projects/MCPL_prediction
source venv/bin/activate
# mlflow models serve -m /home/lenovo/viro/artifact_root/1/5ff27d579438492e9a5bfa59bb5d0a61/artifacts/pipeline -p 1336
#mlflow models serve -m /home/lenovo/Documents/projects/MCPL_prediction/models/artifacts/pipeline -p 1336
mlflow models serve -m ./models/artifacts/pipeline -p 1336
```

Once we have deployed the server (it's running), we can get predictions though a request 

```bash
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["font_size", "rows_number","cols_number", "char_number_text"],"data":[[109, 1291, 730, 46]]}' http://127.0.0.1:1336/invocations
```

### TODO create tag of version v1


