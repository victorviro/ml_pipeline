FROM python:3.9.5

ARG USER_ID
ARG GROUP_ID

RUN groupadd -g ${GROUP_ID} appgroup &&\
    useradd -l -u ${USER_ID} -g appgroup appuser &&\
    install -d -m 0755 -o appuser -g appgroup /home/appuser

RUN apt-get update && apt-get install -y wget && apt-get clean

## Prepare workdir
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME}

COPY docker/mlflow/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.9 -m pip install --upgrade pip
RUN pip3.9 install -r requirements.txt

COPY ./docker/mlflow/entrypoint.sh /usr/local/bin/
RUN chmod gu+x /usr/local/bin/entrypoint.sh && chown appuser:appgroup /usr/local/bin/entrypoint.sh

USER appuser
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
