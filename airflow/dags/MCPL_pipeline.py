# region Imports
import datetime as dt
import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

from src.data.download_raw_data import download_raw_data
from src.data_validation.data_validation import schema_data_validation
from src.models.train_model import data_transformation_and_training
from src.models.model_validation import model_validation

# endregion

# Define the general arguments for the DAG
default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2020, 11, 21),  # Y, M, D
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=10),
}

# Define the DAG
with DAG('max_char_per_line_pipeline',
         default_args=default_args,
         description='',
         schedule_interval='0 0 * * *',
         ) as dag:

    # region Step 0: Helpers
    # Get the airflow variable ml_project (it is a dict)
    MCPL_dict = Variable.get("ml_project", deserialize_json=True)

    # Return the project path (for use later as xcom)
    def get_project_path():
        return os.getcwd()
    return_project_path = PythonOperator(task_id='return_project_path',
                                         python_callable=get_project_path)
    # endregion

    # region Step 1: Data ingestion
    def download_data(*op_args):
        return download_raw_data(op_args[0], op_args[1])

    data_ingestion = PythonOperator(task_id='data_ingestion',
                                    python_callable=download_data,
                                    op_args=[MCPL_dict["MCPL"]["data_name"],  # 'MCPL'
                                             MCPL_dict["MCPL"]["version"]]   # 0
                                    )
    # endregion

    # region Step 2: Data validation
    def val_data(*op_args):
        return schema_data_validation(op_args[0], op_args[1])

    data_validation = PythonOperator(task_id='data_validation',
                                     python_callable=val_data,
                                     op_args=[MCPL_dict["MCPL"]["data_name"],
                                              MCPL_dict["MCPL"]["version"]]
                                     )
    # endregion

    # region Step 3: Data versioning
    data_versioning_command = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    source venv/bin/activate;
    dvc add data/raw/{{ params.data_name }}_data.json;
    dvc push;
    git add data/raw/{{ params.data_name }}_data.json.dvc;
    git commit -m 'ref #410 Added raw data {{ params.data_name }} version \
        {{ params.version }}';
    git push master master
    """

    data_versioning_command_test = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    source venv/bin/activate;
    pwd;
    echo data_name: {{ params.data_name }} version: {{ params.version }};
    """

    # cd /home/lenovo/Documents/projects/ml_quotes_image;
    # source venv/bin/activate;
    # dvc add data/raw/MCPL_data.json;
    # dvc push
    # git add data/raw/MCPL_data.json.dvc;
    # git commit -m 'ref #410 Added raw data MCPL version 0;
    # git push master master

    # {{ var.json.ml_project["MCPL"]["version"] }} == {{ params.version }}

    data_versioning = BashOperator(task_id='data_versioning',
                                   bash_command=data_versioning_command_test,
                                   params=MCPL_dict["MCPL"])
    # {'data_name':'MCPL','version':'0'}
    # endregion

    # region Step 4: Data transformation and training
    def transformation_and_training(*op_args):
        return data_transformation_and_training(op_args[0], op_args[1], op_args[2])
    # return ./models/19e6f5ff3e214460a2adbfca75d25682/artifacts
    data_trans_and_train = PythonOperator(task_id='data_trans_and_train',
                                          python_callable=transformation_and_training,
                                          op_args=[MCPL_dict["MCPL"]["data_name"],
                                                   MCPL_dict["MCPL"]["model"]["alpha"],
                                                   MCPL_dict["MCPL"]["model"]["l1_ratio"]]
                                          )
    # endregion

    # region Step 5: Model validation
    def model_val(*op_args, **context):  # *op_args,
        artifact_path = context['ti'].xcom_pull(task_ids='data_trans_and_train')
        print('artifact_path:', artifact_path)
        model_path = f'{artifact_path}/pipeline/model.pkl'
        return model_validation(op_args[0], model_path)

    model_valid = PythonOperator(task_id='model_valid',
                                 python_callable=model_val,
                                 op_args=[MCPL_dict["MCPL"]["data_name"]],
                                 provide_context=True
                                 )
    # endregion

    # region Step 6: Model versioning
    model_versioning_command = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    source venv/bin/activate;
    dvc add {{ ti.xcom_pull(task_ids='data_trans_and_train') }}/pipeline/model.pkl;
    dvc push;
    git add {{ ti.xcom_pull(task_ids='data_trans_and_train') }}/pipeline/model.pkl.dvc;
    git commit -m 'ref #410 Added model {{ params.data_name }} version \
        {{ params.version }}';
    git push master master
    """
    model_versioning_command_test = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    source venv/bin/activate;
    pwd;
    echo pipeline_path: \
        {{ ti.xcom_pull(task_ids='data_trans_and_train') }}/pipeline/model.pkl;
    echo data_name: {{ params.data_name }} version: {{ params.version }};
    """
    # cd /home/lenovo/Documents/projects/ml_quotes_image;
    # source venv/bin/activate;
    # dvc add models/19e6f5ff3e214460a2adbfca75d25682/artifacts/pipeline/model.pkl;
    # dvc push
    # git add models/19e6f5ff3e214460a2adbfca75d25682/artifacts/pipeline/model.pkl.dvc;
    # git commit -m 'ref #410 Added model MCPL version 0;
    # git push master master

    model_versioning = BashOperator(task_id='model_versioning',
                                    bash_command=model_versioning_command_test,
                                    params=MCPL_dict["MCPL"])
    # {'data_name':'MCPL','version':'0','model':{}}
    # endregion

    # region Step 7: Model deployment
    # TODO analysis for using docker to serve the model in a container
    model_deployment_command = """
    cd {{ ti.xcom_pull(task_ids='return_project_path') }};
    source venv/bin/activate;
    pwd
    """
    # mlflow models serve -m \
    #   {{ ti.xcom_pull(task_ids='data_trans_and_train') }}/pipeline \
    #   -p {{ params.port }};
    # sleep 120
    # #PID=$!
    # sleep 2
    # kill $PID

    # cd /home/lenovo/Documents/projects/ml_quotes_image;
    # source venv/bin/activate;
    # mlflow models serve -m \
    #     ./models/e656214029c54b3ca1e81fde17c72c72/artifacts/pipeline -p 1236

    model_deployment = BashOperator(task_id='model_deployment',
                                    bash_command=model_deployment_command,
                                    params=MCPL_dict["MCPL"]["model_deployment"])

    # endregion

    # region Step 8: Commit and push a tag of the version

    # endregion

(return_project_path >> data_ingestion >> data_validation >> data_versioning
    >> data_trans_and_train >> model_valid >> model_versioning >> model_deployment)
# tag verioning
# monitoring
