FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

## Prepare workdir
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip
RUN pip3.6 install --upgrade pip && pip3.6 install mlflow==1.12.1
RUN pip3.6 install psycopg2==2.8.6

COPY ./docker/mlflow/entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
