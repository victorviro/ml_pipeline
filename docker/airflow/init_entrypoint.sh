
dockerize -wait tcp://postgres:$POSTGRES_PORT -timeout 30s
airflow db init
airflow users create  -u $AIRFLOW_USERNAME -p $AIRFLOW_USER_PASSWORD \
        -r $AIRFLOW_USER_ROLE -f $AIRFLOW_USER_FIRSTNAME -l $AIRFLOW_USER_LASTNAME \
        -e $AIRFLOW_USER_EMAIL
