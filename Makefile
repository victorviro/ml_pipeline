.PHONY: help

include .env

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

ps:
	docker-compose -f ${DOCKER_COMPOSE_FILE} ps
build:
	docker-compose -f ${DOCKER_COMPOSE_FILE} build $(c)
up:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d $(c)
downup: 
	docker-compose -f ${DOCKER_COMPOSE_FILE} down
	docker-compose -f ${DOCKER_COMPOSE_FILE} up --build -d 
start:
	docker-compose -f ${DOCKER_COMPOSE_FILE} start $(c)
down:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down
destroy:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down -v $(c)
stop:
	docker-compose -f ${DOCKER_COMPOSE_FILE} stop $(c)
restart:
	docker-compose -f ${DOCKER_COMPOSE_FILE} stop $(c)
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d $(c)
enter:
	docker exec -it $(c) bash