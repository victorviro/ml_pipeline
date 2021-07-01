# Run the project with docker

First, we [install docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

There are containers for airflow (scheduler, webserver and initialization), mlflow, postgres (with two databases for airflow and mlflow as backend stores), and a container for each pipeline step (see the `docker-compose.yml` file). The dockerfiles used for some containers are in the directory `docker/`.


## Commands


```bash
# List containers
docker ps
# See the logs of a container
docker logs mlflow
# Enter into a container
docker exec -it mlflow bash
# List volumes
docker volume ls
# Remove a specific volume
docker volume rm mcpl_prediction_vol_postres
# List images
docker images
# Remove dangling images
docker image prune
# Inspect a volume
docker volume inspect mcpl_prediction_vol_postres
# Check options for a particular command
docker run --help

# Docker-compose
# Build images 
docker-compose build 
# Build images and up containers
docker-compose up --build -d
# Stop and remove containers
docker-compose down
# Up the container for a service
docker-compose up service
```

**Note**: Some of these commands and more are executed easier using makefile (see file).