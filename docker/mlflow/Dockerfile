FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

## Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 


# Copy the requirements
#ARG PROJECT_SRC
#COPY ${PROJECT_SRC}/requirements.txt /${PROJECT_NAME}/
# RUN pwd

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip
RUN pip3.6 install --upgrade pip && pip3.6 install mlflow==1.12.1
RUN pip3.6 install psycopg2==2.8.6
# -r requirements.txt

# COPY entrypoint.sh /
# RUN chmod gu+x /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]

ARG POSTGRES_MLFLOW_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG MLFLOW_PORT
ARG ARTIFACT_STORE_PATH
ARG MLFLOW_HOST
RUN file="list dir media: $(echo $MLFLOW_PORT)" && echo $file

# CMD mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_MLFLOW_DB \
#         --default-artifact-root $ARTIFACT_STORE_PATH \
#         --host $MLFLOW_HOST 
#        --port $MLFLOW_PORT 
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"