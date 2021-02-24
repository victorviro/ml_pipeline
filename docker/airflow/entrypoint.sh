#!/bin/sh
set -e

airflow users create  --username victorviro --password vikone91 \
    --firstname Victor --lastname Rodeño --role Admin --email vrodeno@ucm.es
airflow db init
airflow webserver -p 8080