###############################
###       ENVIRONMENT       ###
###############################

export PYTHONPATH := $(shell pwd)

-include .env


###############################
###          HELP           ###
###############################

.PHONY: help

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


###############################
###     DOCKER HELPERS      ###
###############################

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


###############################
###    LOCAL DEVELOPMENT    ###
###############################

install:
	python3 -m pip install --upgrade pip
	pip3 install -r requirements/app.txt -r requirements/dev.txt -r requirements/test.txt

install-test:
	python3 -m pip install --upgrade pip
	pip install -r requirements/test.txt

format:
	isort src tests
	black src tests

lint:
	flake8 src tests 
	isort src tests --check-only 
	black src tests --check 
	mypy src tests
	pylint src tests --recursive=y

clean:
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf output
	rm -rf .mypy_cache


###############################
###       CI COMMANDS       ###
###############################

test:
	pytest tests