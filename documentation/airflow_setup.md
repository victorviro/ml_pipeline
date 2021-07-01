# Set up Airflow


First, we need [install airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation.html#).

Airflow needs a home directory (by default it's `~/airflow`). We can set another directory using the environment variable `AIRFLOW_HOME`: 

```bash
export AIRFLOW_HOME=~/airflow
# Check the value of the env variable
echo $AIRFLOW_HOME
```

Now we configure a postgreSQL backend database (instead of sqlite by default). We can follow these [instructions](https://stackoverflow.com/questions/58380835/implementing-postgres-sql-in-apache-airflow) or the [airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-up-database.html#set-up-a-database-backend). 


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

Alternatively, we can set environment variables ([reference](https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html#setting-configuration-options)):
```bash
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
export AIRFLOW__CORE__DAGS_FOLDER=/...
export AIRFLOW__CORE__EXECUTOR=LocalExecutor
```

We can check the current configuration with the `airflow config list` command or `airflow config get-value core sql_alchemy_conn` to check the value of a specific configuration variable.

After configuring the database and connecting to it in Airflow configuration, we create the database schema:

```bash
airflow db init
```

To access to the Airflow webserver we need to [create a user](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#create_repeat1):

```bash
airflow users create  --username airflow --password airflow --firstname Victor --lastname Rodeño --role Admin --email aa@gmail.es
```

Now we can start the webserver (in a new terminal), the default port is 8080.

```bash
airflow webserver -p 8080
```
We also need to start the scheduler (in a new terminal).

```bash
airflow scheduler
```

We can visit localhost:8080 or 0.0.0.0:8080 in the browser and run tasks.

**NOTE**: Press control+c to stop the UI and scheduler

References and further reading:


- [Airflow documentation](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [Production Docker image for Apache Airflow](https://www.youtube.com/watch?v=wDr3Y7q2XoI)
- [Airflow Executors Explained](https://www.astronomer.io/guides/airflow-executors-explained)
- [Own Airflow tutorial](https://github.com/victorviro/airflow_tutorial)
- [Data Pipelines with Apache Airflow](https://www.manning.com/books/data-pipelines-with-apache-airflow)