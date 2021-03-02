#!/bin/sh
set -e


airflow db init
airflow users create  --username victorviro --password vikone91 \
    --firstname Victor --lastname Rodeño --role Admin --email vrodeno@ucm.es
airflow webserver -p 8080