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

```
cd src
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Steps

**NOTE**: In order to run this steps in the pipeline in a airflow DAG we use python functions.

### Get training data / Data Ingestion

Get the dataset through a request to the REST API of the quotes image project.

**NOTE**: Run the backend of the project quotes image to allow the endpoint works:
```
backend/venv/bin/python3.7 backend/manage.py runserver
```

Debug/run via `controller.py`. The file to download the dataset is `src/data/download_raw_data.py`. Stored json data in `data/01_raw/`.

### Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline (building features).

Debug/run via `controller.py`. The file to validate the schema of the dataset is `src/data_validation/schema_validation.py`.


TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).

### DVC versioning the data

To see the steps as in the first time we run the project, in the reference documentation in `references/DVC_data_versioning.md`.

Run `dvc add` again to track the latest version.

```bash
dvc add data/01_raw/Data_test.json
```

Usually we would also run `git commit` and `dvc push` to save the changes:

```bash
# Using the command line
git add data/01_raw/Data_test.json.dvc
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

`mlflow ui`

### Model versioning

The file to train the model outputs the artifact uri (`./mlruns/0/1c.../artifacts`). Once the model is validated, we track this directory with DVC. We first copy the artifact dir to `models/`:

```bash
cp -R /home/lenovo/Documents/projects/MCPL_prediction/mlruns/2/ca63e95ea1f0426c835d94c8f29334e2/artifacts /home/lenovo/Documents/projects/MCPL_prediction/models/
dvc add /home/lenovo/Documents/projects/MCPL_prediction/models/artifacts
```

Usually we would also run `git commit` and `dvc push`.


### Model deployment

The `mlflow.sklearn.log_model(pipe, "pipeline")` produced two files in `./mlruns/0/1c.../artifacts/pipeline/` (the full path in the view of that artifact in the UI) (the directory `1c...` depicts the run_id, it will be different for you):

- `MLmodel`, is a metadata file that tells MLflow how to load the model.
- `model.pkl`, is a serialized version of the linear regression model that we trained.

In this example, we can use this MLmodel format with MLflow to deploy a local REST server that can serve predictions. To deploy the server, run (replace the path with your model’s actual path):

open in a new window command:
```
cd Documents/projects/ml_quotes_image
source venv/bin/activate
```
```
mlflow models serve -m file:///home/lenovo/Documents/projects/ml_quotes_image/mlruns/0/02fa5dfe2f474ab48f7c9a5c57c0468c/artifacts/pipeline -p 1236
```
or
```
mlflow models serve -m /home/lenovo/Documents/projects/ml_quotes_image/mlruns/0/02fa5dfe2f474ab48f7c9a5c57c0468c/artifacts/pipeline -p 1236
```


or
```
mlflow models serve -m ./mlruns/0/02fa5dfe2f474ab48f7c9a5c57c0468c/artifacts/pipeline -p 1236
```
Once we have deployed the server (it's running), we can get predictions though a request passing some sample data. The following example uses curl to send a JSON-serialized pandas DataFrame with the split orientation to the model server. More information about the input data formats accepted by the model server, see the [MLflow deployment tools documentation](https://www.mlflow.org/docs/latest/models.html#local-model-deployment).

```
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["font_size", "rows_number","cols_number", "char_number_text"],"data":[[109, 1291, 730, 46]]}' http://127.0.0.1:1236/invocations

```

### TODO create tag of version v1