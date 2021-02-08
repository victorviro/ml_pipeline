ML_quotes_image
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

### Get training data / Data Ingestion

**NOTE**: Run the backend of the project quotes image to allow the endpoint works:
```
backend/venv/bin/python3.7 backend/manage.py runserver
```

Run script 

```
python src/data/download_raw_data.py --data_name MCPL --version 1
```

Stored json data in `data/raw`.

**NOTE**: In order to run this step of the pipeline in a airflow DAG we use a python functions instead to run the script as we saw previously. If we want to run this step via line command descomment the code `#@click.command()` inside the script before.

TODO: add execution to the makefile.

### Data validation

Check the schema of the dataset downloaded using pandera since data must be validated before versioning it and go to the next step in the pipeline (building features)

```
source venv/bin/activate
python src/data_validation/data_validation.py --data_name MCPL --version 1
```

**NOTE**: In order to run this step of the pipeline in a airflow DAG we use a python functions instead to run the script as we saw previously. If we want to run this step via line command descomment the code `#@click.command()` inside the script before.

TODO: Validate distribution of target variable, statistics of the dataset variables (like do TFX).

### DVC versioning the data
Let's explain the steps as this is the first time we run the project:

`dvc init`

A new `.dvc/` directory is created for internal configuration. This directory is automatically staged with `git add`, so it can be easily committed with Git.

We add a new local [data remote](https://dvc.org/doc/command-reference/remote/add):

```
dvc remote add -d local_storage /tmp/dvc-storage
```
This command creates a remote section in the DVC project's config file with name `local_storage` and url `/tmp/dvc-storage`. We commit and push this directory.

Let's capture the current state of this dataset adding it to DVC tracking:
```
dvc add data/raw/MCPL_data_v1.json
```

A metadata file `data/raw/MCPL_data_v1.json.dvc` is added in the directory (this file is not the dataset itself, it's a metadata file that contains the hash (md5) of the dataset and the path). Later we can convert this file to the dataset.

Let's commit this file to the git repo:

```
git add data/raw/MCPL_data_v1.json.dvc
git commit -m "Added raw data (max_char_per_line training raw data)"
#push
```

Now we have the dataset which has been tracked by dvc but the dataset is in our directory and we could want to push it into our own remote storage. Now we push the dvc repo to get the data in the local_storage directory (`tmp/dvc-storage`)

```
dvc push
```

Let's remove the dataset (and clear cache) in our directory to show how we can pull it.

```
# removed datasets tracked bu dvc
rm -rf .dvc/cache
```

We can use `dvc pull` and that is going to download a new copy of the dataset into our directory (`data/raw/MCPL_data_v1.json`).

Info links:

- [`dvc list <url>`](https://dvc.org/doc/command-reference/list)

- [dvc status](https://dvc.org/doc/command-reference/status)



### Notebooks (EDA dataset)

`pip install jupyter`

launch jupyter in other window:
```
cd Documents/projects/MCPL_prediction
source venv/bin/activate
jupyter notebook
```
select interpreter
create a notebook via command pallete in vscode (Create new blank jupyter notebook) save it where we want (we have already saved a notebook for EDA in `notebooks/EDA_MCPL_data.ipynb`).

[Docu jupyter notebook in VScode](https://code.visualstudio.com/docs/python/jupyter-support#_save-your-jupyter-notebook) 

### Preprocessing the data

- Added custom transformation for sklearn to use in pipeline (ratio_cols_rows).
- Normalized features in pipeline when training the model


### Train the model

Run script

```
python src/models/train_model.py
```

```
python src/models/train_model.py --alpha 0.0098 --l1_ratio 0.4
python src/models/train_model.py --alpha 0.8 --l1_ratio 0.1
```

**NOTE**: In order to run this step of the pipeline in a airflow DAG we use a python function instead to run the script as we saw previously. If we want to run this step via line command descomment the code `#@click.command()` inside the script before.

#### Comparing the models

`mlflow ui`

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

