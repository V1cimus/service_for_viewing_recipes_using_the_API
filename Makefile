DOCKER_COMPOSE_DIR := infra/
export DOCKER_USERNAME := $(shell sed 'DOCKER_USERNAME=' .env)

up:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker pull $(DOCKER_USERNAME)/foodgram_backend:latest && \
	sudo docker-compose up -d && \
	sudo docker image prune -f

down:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose down -v

clean:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose down --rmi all --volumes --remove-orphans

rm_web:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose stop && \
	sudo docker image rm $(DOCKER_USERNAME)/foodgram_backend

migrate:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py migrate
    
collectstatic:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py collectstatic --no-input

localisation:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py compilemessages --no-input