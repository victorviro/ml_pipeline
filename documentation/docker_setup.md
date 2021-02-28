# Run the project with docker

At the moment, two containers are up (todo: add a container for airflow).

- `mlflow` container. It contains the project and serves the mlflow ui

- `postgres` container. It store the experiments info of mlflow (in the future it will store info of airflow pipelines)

See the `mcpl_prediction/docker-compose.yml` file. The dockerfiles for both containers are in `docker/`.

## Set up
```bash
# Build images and up containers
docker-compose up --build -d
# List containers
docker ps
# Stops containers and removes containers
docker-compose down
# See the logs of the container
docker logs mlflow
docker logs postgres
# Enter into a container
docker exec -it mlflow bash
# List volumes
docker volume ls
# Remove a specific volume
docker volume rm mcpl_prediction_vol_postres1
# Stop postgresql service
sudo service postgresql stop
```