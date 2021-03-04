FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

# Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Copy the requirements
ARG PROJECT_SRC
# RUN file="list dir media: $(echo $PROJECT_SRC)" && echo $file
COPY ${PROJECT_SRC}/validate_data_schema/infrastructure/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip
RUN pip3.6 install --upgrade pip && pip3.6 install -r requirements.txt

# COPY ${PROJECT_SRC}/validate_data_schema/ ${PROJECT_SRC}/validate_data_schema/

ARG PORT_VALIDATE_DATA
ARG HOST_USE_CASES_APIS
CMD uvicorn src.validate_data_schema.infrastructure.pandera_schema_validator_api:rest_api \
    --host $HOST_USE_CASES_APIS --port $PORT_VALIDATE_DATA
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"