FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

# Install dockerize to avoid startup problems (waiting for DB to start)
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz \
         -O - | tar -C /usr/local/bin -xzv

## Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 


# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip==20.2.4
RUN pip3.6 install apache-airflow==2.0.1 && pip3.6 install psycopg2==2.8.6

RUN pwd
RUN export AIRFLOW_HOME=~/airflow
# /root/airflow/
RUN pwd
#RUN echo "sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost:5432/airflow" >> /airflow/airflow.cfg
#RUN echo "dags_folder = /home/lenovo/Documents/projects/mcpl_prediction/airflow/dags" >> /airflow/airflow.cfg

COPY airflow/airflow.cfg /root/airflow/

ARG POSTGRES_AIRFLOW_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG AIFLOW_PORT
# RUN file="list dir media: $(echo $POSTGRES_USER)" && echo $file

#RUN airflow db init
# RUN airflow users create  --username victorviro --password vikone91 \
#     --firstname Victor --lastname Rodeño --role Admin --email vrodeno@ucm.es
CMD airflow db init && airflow webserver -p $AIFLOW_PORT
#http://0.0.0.0:8080/
#psql -h postgres -p 5432 -d mcpl_airflow_db -U postgres_user
