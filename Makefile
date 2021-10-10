.PHONY: help
export PYTHONPATH := $(shell pwd)

-include .env

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

ps:
	docker-compose -f ${DOCKER_COMPOSE_FILE} ps

build:
	docker-compose -f ${DOCKER_COMPOSE_FILE} build $(c)
	
up:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d $(c)

buildup: build up

down:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down

downup: down buildup

start:
	docker-compose -f ${DOCKER_COMPOSE_FILE} start $(c)

destroy:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down -v $(c)

stop:
	docker-compose -f ${DOCKER_COMPOSE_FILE} stop $(c)

restart: stop up

enter:
	docker exec -it $(c) bash

# https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html#initializing-environment
init-airflow: 
	make buildup c=postgres 
	make buildup c=airflow-init 

install-test:
	python3 -m pip install --upgrade pip
	pip install -r requirements/test.txt

test:
	pytest tests

format:
	isort src tests
	black src tests

lint:
	flake8 src tests 
	isort src tests --check-only 
	black src tests --check 
	find src tests -name "*.py" ! -name '__init__.py' ! -name 'conftest.py' | xargs pylint --exit-zero

clean:
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf output