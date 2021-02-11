"""
Example passing xcoms between python operatorts and between python and bash operators

https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/
https://stackoverflow.com/questions/54638295/i-cant-xcom-push-an-arguments-through-bashoperator/54641778

and using variables
https://airflow.apache.org/docs/stable/concepts.html?highlight=xcom#variables
"""

import datetime as dt
import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable




default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2020, 11, 20), #year, month, day
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('airflow_tutorial_v01',
         default_args=default_args,
         description='A simple tutorial DAG',
         schedule_interval='0 0 * * *',
         ) as dag:
    
    MCPL_dict = Variable.get("ml_project", deserialize_json=True)
    def print_root_path(*op_args):
        #print(f'Root path: {os.getcwd()}')
        print('====='*6)
        print(op_args[0]["MCPL"])
        return os.getcwd()

    print_path = PythonOperator(task_id='print_root_path',
                                 python_callable=print_root_path,
                                 op_args = [MCPL_dict])

    def print_root_path2(**context):
        print('====='*6)
        print(context['ti'].xcom_pull(task_ids='print_root_path'))
        print('====='*6)

    # print_path2 = PythonOperator(task_id='print_root_path2',
    #                              python_callable=print_root_path2,
    #                              provide_context=True)



    command = """
    cd {{ ti.xcom_pull(task_ids='print_root_path') }}; 
    pwd
    echo {{ var.json.ml_project["MCPL"] }}
    """
    #export A={{ var.json.ml_project }};
    #echo $A
    print_path2 = BashOperator(task_id='print_root_path2',
                         bash_command=command)



print_path >> print_path2
#print_path2