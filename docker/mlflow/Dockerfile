FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

## Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 


# Copy the requirements
ARG PROJECT_SRC
COPY ${PROJECT_SRC}/requirements.txt /${PROJECT_NAME}/
# RUN pwd

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip
RUN pip3.6 install --upgrade pip && pip3.6 install -r requirements.txt


# COPY entrypoint.sh /
# RUN chmod gu+x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

#CMD ["rails", "server", "-b", "0.0.0.0"]
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG MLFLOW_PORT
ARG ARTIFACT_STORE_PATH
ARG MLFLOW_HOST

CMD mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$MLFLOW_HOST/$POSTGRES_DB \
        --default-artifact-root $ARTIFACT_STORE_PATH \
        --host $MLFLOW_HOST \
        --port $MLFLOW_PORT 
