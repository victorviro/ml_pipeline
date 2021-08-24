FROM python:3.9.5

ARG USER_ID
ARG GROUP_ID

RUN groupadd -g ${GROUP_ID} appgroup &&\
    useradd -l -u ${USER_ID} -g appgroup appuser &&\
    install -d -m 0755 -o appuser -g appgroup /home/appuser

RUN apt-get update && apt-get install -y wget python3-pip && apt-get clean

# Prepare workdir
ARG PROJECT_NAME
RUN mkdir ${PROJECT_NAME}
WORKDIR ${PROJECT_NAME} 

# Copy the requirements
ARG PROJECT_SRC
COPY ${PROJECT_SRC}/notebooks/requirements.txt /${PROJECT_NAME}/

# Update pip and install requirements
RUN python3.9 -m pip install --upgrade pip
RUN pip3.9 install --upgrade pip && pip3.9 install -r requirements.txt

USER appuser
CMD jupyter notebook --port=$JUPYTER_PORT --no-browser --ip=$JUPYTER_HOST --allow-root
