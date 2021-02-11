### Model deployment

In this document, we explain how to deploy a model previously tracked by MLflow.

The `mlflow.sklearn.log_model(pipe, "pipeline")` produced two files in `..../artifacts/pipeline/` (the full path in the view of that artifact in the UI) (the directory `1c...` depicts the run_id, it will be different for you):

- `MLmodel`, is a metadata file that tells MLflow how to load the model.
- `model.pkl`, is a serialized version of the model that we trained.

In this example, we can use this `MLmodel` format with MLflow to deploy a local REST server that can serve predictions. To deploy the server, run (replace the path with your model’s actual path) in a separate command line:


```bash
cd ...
source venv/bin/activate
mlflow models serve -m /home/lenovo/Documents/projects/ml_quotes_image/mlruns/0/02fa5dfe2f474ab48f7c9a5c57c0468c/artifacts/pipeline -p 1236
# mlflow models serve -m ./mlruns/0/02fa5dfe2f474ab48f7c9a5c57c0468c/artifacts/pipeline -p 1236
```
Once we have deployed the server (it's running), we can get predictions through a request passing some sample data. The following example uses curl to send a JSON-serialized pandas DataFrame with the split orientation to the model server. More information about the input data formats accepted by the model server, see the [MLflow deployment tools documentation](https://www.mlflow.org/docs/latest/models.html#local-model-deployment).

```bash
curl -X POST -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["font_size", "rows_number","cols_number", "char_number_text"],"data":[[109, 1291, 730, 46]]}' http://127.0.0.1:1236/invocations
```