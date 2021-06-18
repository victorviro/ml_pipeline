FROM python:3.9.5

RUN apt-get update && apt-get install -y wget && apt-get clean

# Prepare workdir
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Copy the requirements
ARG PROJECT_SRC
COPY ${PROJECT_SRC}/notebooks/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.9 -m pip install --upgrade pip
RUN pip3.9 install --upgrade pip && pip3.9 install -r requirements.txt

CMD jupyter notebook --port=$JUPYTER_PORT --no-browser --ip=$JUPYTER_HOST --allow-root
