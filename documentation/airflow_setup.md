# Set up Aiflow


[Install airflow via pip](https://airflow.apache.org/docs/apache-airflow/stable/installation.html#installation-tools) (not needed if we installed `src/requirements.txt`):

Airflow needs a home, by default it's ~/airflow.

```bash
export AIRFLOW_HOME=~/airflow
# Check the value of the variable
echo $AIRFLOW_HOME
```

We can create a user, run `airflow db init` and up the airflow web server and scheduler, but first we setup the postgres backend db (instead of sqlite by default). We can follow these [intructions](https://stackoverflow.com/questions/58380835/implementing-postgres-sql-in-apache-airflow). 

For example, to create a database `airflow` with password `airflow` and a db `airflow` in postgre console (more info in sublime docs postgres):

```bash
sudo -u postgres psql
CREATE USER airflow WITH ENCRYPTED PASSWORD 'airflow';
CREATE DATABASE airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
```


We have to do some changes in the in `airflow.cgf` conf file (inside airflow home directory) file:
```bash
# Define our dags folder
dags_folder = /home/lenovo/Documents/projects/mcpl_prediction/airflow/dags

# Define our postgre db
#sql_alchemy_conn = postgresql+psycopg2://user:pass@hostadress:port/database
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow
```

We need to initialize the database again to apply the changes:

```bash
# airflow initdb in airflow<2
airflow db init
```

Now we can start the web server (in a new terminal), the default port is 8080
```bash
cd Documents/projects/mcpl_prediction
source venv/bin/activate
airflow webserver -p 8080
```
We can also start the scheduler (in a new terminal) (needed to run tasks)
```
cd Documents/projects/mcpl_prediction
source venv/bin/activate
airflow scheduler
```
We can visit localhost:8080 or 0.0.0.0:8080 in the browser and run tasks
**NOTE**: Press control+c to stop the ui and scheduler

In order to acess to the Airflow web server we need to [Create a user](https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#create_repeat1):

```bash
airflow users create  --username victorviro --password vikone91 --firstname Victor --lastname Rodeño --role Admin --email vrodeno@ucm.es
```



Info:
- [how-to-use-apache-airflow-in-a-virtual-environment](https://stackoverflow.com/questions/56890937/how-to-use-apache-airflow-in-a-virtual-environment)
- [Tuto airflow](https://airflow-tutorial.readthedocs.io/en/latest/first-airflow.html)
- [Issue changing the airflow_home env variable](https://stackoverflow.com/questions/57515434/why-do-i-get-no-such-table-error-when-installing-apache-airflow-on-mac)
airflow WARNING - Failed to log action with (sqlite3.OperationalError) no such table

- [Viro Airflow tutorial](https://github.com/victorviro/airflow_tutorial)

- Example simple dag called: `airflow_tutorial_v01.py`. Explained in [repo](https://github.com/victorviro/airflow_tutorial) (modified in this repo to use xcoms and airflow variables)


- [Airflow bash_operator tuto](https://marclamberti.com/blog/airflow-bashoperator/)
- [Best practices pythonoperators or bashoperators](https://stackoverflow.com/questions/47534414/apache-airflow-best-practice-pythonoperators-or-bashoperators)
- [Airflow Python operator passing parameters](https://stackoverflow.com/questions/54717221/airflow-python-operator-passing-parameters)

- [airflow-xcoms-examples](https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/)






Note: When running server airflow: if airflow Error: Already running on PID
Run `ps aux | grep airflow` and check if `airflow webserver` or process is running. If it is, kill them and rerun
`kill -9 PID_NUMBER` 
because control+z was used to go out of the server (use control+c instead)

`ps aux | grep mlflow`