include .env

up:
	docker compose -f ${DOCKER_COMPOSE_FILE} up -d
down:
	docker compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans
scraping:
	docker compose -f ${DOCKER_COMPOSE_FILE} exec scraping /bin/bash
ps:
	docker compose -f ${DOCKER_COMPOSE_FILE} ps -a
