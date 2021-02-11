
- [Tutorial Airflow](https://github.com/victorviro/airflow_tutorial)

## Install Airflow
We activate the environment, and install airflow via pip:

```
source venv/bin/activate
pip install apache-airflow==1.10.12 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
```
or
```
pip install \
 apache-airflow[postgres,gcp]==1.10.12 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.7.txt"
```
Airflow needs a home, by default it's ~/airflow.

```
#export AIRFLOW_HOME=/home/lenovo/Documents/projects/ml_quotes_image/airflow # gives error later
export AIRFLOW_HOME=~/airflow
```

We can check the value of the variable with bash:

```
echo $AIRFLOW_HOME
```

After configuration, we need to initialize the database before we can run tasks (using DB sqlite by default):

```
airflow initdb
```

We use postgresql instead of sqlite. Follow [intructions](https://stackoverflow.com/questions/58380835/implementing-postgres-sql-in-apache-airflow) (to create a database `airflow` with password `airflow` and a db `airflow`).

```
CREATE USER airflow WITH ENCRYPTED PASSWORD 'airflow';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```


We do some changes in the in airflow.cgf (inside airflow home directory) file:
```
# Define our dags folder
dags_folder = /home/lenovo/Documents/projects/ml_quotes_image/airflow/dags

# Define our postgre db
#sql_alchemy_conn = postgresql+psycopg2://user:pass@hostadress:port/database
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
```
We need to initialize the database again to apply the changes:

```
airflow initdb
```

## Initialize Airflow

Now we can start the web server (in a new terminal), the default port is 8080
```
cd Documents/projects/ml_quotes_image
source venv/bin/activate
airflow webserver -p 8080
```
We can also start the scheduler (in a new terminal) (necessary tu run tasks)
```
cd Documents/projects/ml_quotes_image
source venv/bin/activate
airflow scheduler
```
We can visit localhost:8080 or 0.0.0.0:8080 in the browser and run tasks
**NOTE**: Press control+c to stop the ui and scheduler

Info:
- [how-to-use-apache-airflow-in-a-virtual-environment](https://stackoverflow.com/questions/56890937/how-to-use-apache-airflow-in-a-virtual-environment)
- [Tuto airflow](https://airflow-tutorial.readthedocs.io/en/latest/first-airflow.html)
- [Issue changing the airflow_home env variable](https://stackoverflow.com/questions/57515434/why-do-i-get-no-such-table-error-when-installing-apache-airflow-on-mac)
airflow WARNING - Failed to log action with (sqlite3.OperationalError) no such table

## DAGS

- Example simple dag called: `airflow_tutorial_v01.py`. Explained in [repo](https://github.com/victorviro/airflow_tutorial) (modified to use xcoms and airflow variables)

- `MCPL_pipeline`


Info:
- [bash_operator tuto](https://marclamberti.com/blog/airflow-bashoperator/)
- [best-practice-pythonoperators-or-bashoperators](https://stackoverflow.com/questions/47534414/apache-airflow-best-practice-pythonoperators-or-bashoperators)
- [Airflow Python operator passing parameters](https://stackoverflow.com/questions/54717221/airflow-python-operator-passing-parameters)

- [airflow-xcoms-examples](https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/)






Note: When running server airflow: if airflow Error: Already running on PID
Run `ps aux | grep airflow` and check if `airflow webserver` or process is running. If it is, kill them and rerun
`kill -9 PID_NUMBER` 
because control+z was used to go out of the server (use control+c instead)

`ps aux | grep mlflow`