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

ENV AIRFLOW_HOME=~/airflow
# /root/airflow/

ARG POSTGRES_AIRFLOW_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_PORT
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://$POSTGRES_USER:\
$POSTGRES_PASSWORD@postgres:$POSTGRES_PORT/$POSTGRES_AIRFLOW_DB



ARG AIFLOW_PORT
# RUN file="list dir media: $(echo $POSTGRES_USER)" && echo $file


COPY /docker/airflow docker/airflow
RUN chmod 755 /mcpl_prediction/docker/airflow/entrypoint.sh
ENTRYPOINT ["/mcpl_prediction/docker/airflow/entrypoint.sh"]
