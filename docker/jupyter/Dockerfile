FROM python:3.6.9

RUN apt-get update && apt-get install -y wget && apt-get clean

# Prepare workdir (mcpl_prediction)
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Copy the requirements
ARG PROJECT_SRC
COPY ${PROJECT_SRC}/notebooks/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN apt-get update && apt-get install -y python3-pip
RUN python3.6 -m pip install --upgrade pip
RUN pip3.6 install --upgrade pip && pip3.6 install -r requirements.txt


ARG JUPYTER_PORT
ARG JUPYTER_HOST
ENV JUPYTER_PORT=$JUPYTER_PORT
ENV JUPYTER_HOST=$JUPYTER_HOST
CMD jupyter notebook --port=$JUPYTER_PORT --no-browser --ip=$JUPYTER_HOST --allow-root
# jupyter notebook --port=8888 --ip=0.0.0.0 --no-browser --allow-root
