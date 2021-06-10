FROM python:3.9.5

RUN apt-get update && apt-get install -y wget && apt-get clean

# Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN file="list dir media: $(echo $PROJECT_NAME)" && echo $file
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Copy the requirements

ARG PROJECT_SRC
ARG USE_CASE
RUN file="list dir media: $(echo $USE_CASE)" && echo $file
COPY ${PROJECT_SRC}/${USE_CASE}/infrastructure/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip && apt-get install python3-dev
RUN python3.9 -m pip install --upgrade pip
RUN pip3.9 install --upgrade pip && pip3.9 install -r requirements.txt
 
# COPY ${PROJECT_SRC}/${USE_CASE}/ ${PROJECT_SRC}/${USE_CASE}/
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"