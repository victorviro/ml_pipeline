# Postgre as backend store in MLflow

We use PostgreSQL database as a backend store. 

## Install mlflow

```bash
pip install mlflow==1.12.1
pip install psycopg2==2.8.6
```

## Create database and user

Lets use the command line with psql:
```bash
sudo -u postgres psql
```
In the postgres console, we create a database `mlflow_db`, and a user `mlflow_user` with password `mlflow`:

```bash
# Create a new database
CREATE DATABASE mlflow_db;
# Check database was created:
\l
# Create a user
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
# Check user was created: 
\du
# Give privileges for the mlflow_db to this user
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```

## Launch mlflow tracking server


The database needs to be encoded as `dialect+driver://username:password@host:port/database`.

```bash
mlflow server --backend-store-uri postgresql://mlflow_user:mlflow@localhost/mlflow_db \
        --default-artifact-root /artifact_store \
        --host 0.0.0.0 \
        --port 5000 
```

In this case we have two store locations: `--backend-store-uri` for everything except artifacts (the db) and `--default-artifact-root` for artifacts only. 

Now the Tracking server should be available at the following URL: http://0.0.0.0:5000.

We can set the tracking URI at the beginning of our program, with the same `host:port` as we used to configure the mlflow server (`mlflow.set_tracking_uri('http://0.0.0.0:5000')`) or we can do it with the CLI setting the following environment variable:

```bash
export MLFLOW_TRACKING_URI='http://0.0.0.0:5000'
```

## References

- [MLflow Tracking Servers](https://www.mlflow.org/docs/latest/tracking.html#mlflow-tracking-servers)