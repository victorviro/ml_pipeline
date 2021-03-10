# Set up Aiflow


[Install airflow via pip](https://airflow.apache.org/docs/apache-airflow/stable/installation.html#).

Airflow needs a home, by default it's ~/airflow.

```bash
export AIRFLOW_HOME=~/airflow
# Check the value of the env variable
echo $AIRFLOW_HOME
```

We can create a user, run `airflow db init` and up the airflow web server and scheduler, but first we configure the postgres backend db (instead of sqlite by default). We can follow these [instructions](https://stackoverflow.com/questions/58380835/implementing-postgres-sql-in-apache-airflow) or the [airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#set-up-a-database-backend). 

For example, to create a database `airflow` with password `airflow` and a db `airflow` in postgre console (more info in sublime docs postgres):

```bash
sudo -u postgres psql
CREATE USER airflow WITH ENCRYPTED PASSWORD 'airflow';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```


We do some changes in the in `airflow.cgf` configuration file (inside airflow home directory):
```bash
# Define the dags folder
dags_folder = /...
# Define the postgre db connection
# sql_alchemy_conn = postgresql+psycopg2://user:pass@hostadress:port/database
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
# Define the executor
executor = LocalExecutor
```

Alternatively, we can set env variables ([reference](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html#setting-configuration-options)):
```bash
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
export AIRFLOW__CORE__DAGS_FOLDER=/...
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
```

We can check the current configuration with the `airflow config list` command or `airflow config get-value core sql_alchemy_conn` to check the value of a specific configuration variable.


We need to initialize the database again to apply the changes:

```bash
airflow db init
# For airflow < 2 
airflow initdb
```

Now we can start the web server (in a new terminal), the default port is 8080
```bash
airflow webserver -p 8080
```
We need also start the scheduler (in a new terminal).
```bash
airflow scheduler
```
We can visit localhost:8080 or 0.0.0.0:8080 in the browser and run tasks
**NOTE**: Press control+c to stop the ui and scheduler

In order to acess to the Airflow web server we need to [create a user](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#create_repeat1):

```bash
airflow users create  --username airflow --password airflow --firstname Victor --lastname Rodeño --role Admin --email aa@gmail.es
```

Info:

- [Airflow tutorial](https://airflow-tutorial.readthedocs.io/en/latest/first-airflow.html)
- [Own Airflow tutorial](https://github.com/victorviro/airflow_tutorial)
- [Airflow bash_operator tuto](https://marclamberti.com/blog/airflow-bashoperator/)
- [Airflow xcoms examples](https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/)
- [Production Docker image for Apache Airflow](https://www.youtube.com/watch?v=wDr3Y7q2XoI)
- [Airflow Executors Explained](https://www.astronomer.io/guides/airflow-executors-explained)



Note: When running server airflow: if `airflow Error: Already running on PID`
Run `ps aux | grep airflow` and check if `airflow webserver` or process is running. If it is, kill them and re-run
`kill -9 PID_NUMBER` 
Cause: control+z was used to go out of the server (use control+c instead).

