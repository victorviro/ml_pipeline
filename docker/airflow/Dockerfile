FROM python:3.9.5

ARG USER_ID
ARG GROUP_ID

RUN groupadd -g ${GROUP_ID} appgroup &&\
    useradd -l -u ${USER_ID} -g appgroup appuser &&\
    install -d -m 0755 -o appuser -g appgroup /home/appuser

RUN apt-get update && apt-get install -y wget python3-pip && apt-get clean

# Install dockerize to avoid startup problems (waiting for DB to start)
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz \
    -O - | tar -C /usr/local/bin -xzv

## Prepare workdir
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

COPY docker/airflow/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN python3.9 -m pip install --upgrade pip
RUN pip3.9 install -r requirements.txt

COPY docker/airflow/init_entrypoint.sh /${PROJECT_NAME}/docker/airflow/init_entrypoint.sh
RUN chown appuser:appgroup /${PROJECT_NAME}/docker/airflow/init_entrypoint.sh

ARG AIRFLOW_HOME
RUN mkdir -pv ${AIRFLOW_HOME}; \
    chown -R appuser:appgroup ${AIRFLOW_HOME};
USER appuser