include .env

up:
	docker compose -f ${DOCKER_COMPOSE_FILE} up -d
down:
	docker compose -f ${DOCKER_COMPOSE_FILE} down --remove-orphans
scraping:
	docker compose -f ${DOCKER_COMPOSE_FILE} exec scraping /bin/bash
db:
	docker compose -f ${DOCKER_COMPOSE_FILE} exec db mysql -h 127.0.0.1 -u${MYSQL_USER} -p${MYSQL_PASSWORD}
ps:
	docker compose -f ${DOCKER_COMPOSE_FILE} ps -a
destroy:
	docker compose -f ${DOCKER_COMPOSE_FILE} down --rmi all --volumes --remove-orphans
