# Run the project with docker

At the moment, there are containers for airflow (scheduler, webserver and initialization), mlflow, postgres (with two databases for airflow and mlflow as backend stores), and containers for use cases (see the `docker-compose.yml` file). The dockerfiles used for some containers are in `docker/`.


## Set up and docker commands

Install docker and docker-compose.

```bash
# Build images and up containers
docker-compose up --build -d
# List containers
docker ps
# Stop containers and remove containers
docker-compose down
# See the logs of the container
docker logs mlflow
# Enter into a container
docker exec -it mlflow bash
# List volumes
docker volume ls
# Remove a specific volume
docker volume rm mcpl_prediction_vol_postres
# Stop postgresql service
sudo service postgresql stop
# Up the container for a service
docker-compose up service
# List images
docker images
# Remove dangling images
docker image prune

docker volume inspect mcpl_prediction_vol_postres

sudo rm -rf src/airflow_dags/logs/max_char_per_line_apis
```