# Postgre as backend store in MLflow

We can use PostgreSQL database as a backend store. After install it, we need to set it up...

## Create database and user
Lets use the command line with psql:
```bash
sudo -u postgres psql
```
In the postgre console, we create a database mcpl_mlflow_db, and a user mlflow_user with password mlflow:

```bash
# create a new database (in the postgre console run:)
CREATE DATABASE mcpl_mlflow_db;
# check database created: 
\l
# Create a user
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
# check created user: 
\du
# give privileges for the mlflow_db to this user
GRANT ALL PRIVILEGES ON DATABASE mcpl_mlflow_db TO mlflow_user;
# connect to the database to see tables in the database
\c mcpl_mlflow_db
# show tables in the current schema
\dt
# show the table metrics (once there are experiments run)
select * from metrics;
```

## Create artifact store

We create a local folder to store the artifacts: `home/viro/artifact_root`

In this case we have two store locations: `--backend-store-uri` for everything except artifacts (the db) and `--default-artifact-root` for artifacts only (the location we just defined/created). 

## Launch mlflow uri

We need install psycopg2 with `pip install psycopg2`.

The database needs to be encoded as `dialect+driver://username:password@host:port/database`.

```bash
mlflow server --backend-store-uri postgresql://mlflow_user:mlflow@localhost/mcpl_mlflow_db \
        --default-artifact-root file:/home/lenovo/viro/artifact_root \
        --host 0.0.0.0 \
        --port 5000 
```

Now the Tracking server should be available at the following URL: http://0.0.0.0:5000.

We can set the tracking URI at the beginning of our program, with the same host:port as we used to configure the mlflow server (`mlflow.set_tracking_uri('http://0.0.0.0:5000')`) or we can do it with the CLI setting the following environmental variable:

```bash
export MLFLOW_TRACKING_URI='http://0.0.0.0:5000'
```


