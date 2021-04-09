#!/bin/sh
set -e

mlflow server --backend-store-uri $MLFLOW_SQL_ALCHEMY_CONN \
    --default-artifact-root $ARTIFACT_STORE_PATH \
    --host $MLFLOW_HOST \
    --port $MLFLOW_PORT
