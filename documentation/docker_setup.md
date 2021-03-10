# Run the project with docker

There are containers for airflow (scheduler, webserver and initialization), mlflow, postgres (with two databases for airflow and mlflow as backend stores), and a container for each pipeline step (see the `docker-compose.yml` file). The dockerfiles used for some containers are in `docker/`.


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
# Up the container for a service
docker-compose up service
# List images
docker images
# Remove dangling images
docker image prune
# Inspecto a volume
docker volume inspect mcpl_prediction_vol_postres
# Other useful commands
# Stop postgresql service
sudo service postgresql stop
# Remove airflow logs
sudo rm -rf src/airflow_dags/logs/max_char_per_line_apis
```