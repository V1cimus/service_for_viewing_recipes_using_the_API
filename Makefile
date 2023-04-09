DOCKER_COMPOSE_DIR := infra/

up:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker pull ${ secrets.DOCKER_USERNAME }/foodgram_backend:latest && \
	sudo docker-compose up -d && \
	sudo docker image prune -f

down:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose down -v

clean:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose down --rmi all --volumes --remove-orphans

env:
	cd $(DOCKER_COMPOSE_DIR) && \
	touch .env && \
	echo DB_ENGINE=${ secrets.DB_ENGINE } > .env && \
	echo DB_NAME=${ secrets.DB_NAME } >> .env && \
	echo POSTGRES_USER=${ secrets.POSTGRES_USER } >> .env && \
	echo POSTGRES_PASSWORD=${ secrets.POSTGRES_PASSWORD } >> .env && \
	echo DB_HOST=${ secrets.DB_HOST } >> .env && \
	echo DB_PORT=${ secrets.DB_PORT } >> .env && \
	echo DEBUG=${ secrets.DEBUG } >> .env

rm_web:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose stop && \
	sudo docker image rm ${ secrets.DOCKER_USERNAME }/foodgram_backend

migrate:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py migrate
    
collectstatic:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py collectstatic --no-input

localisation:
	cd $(DOCKER_COMPOSE_DIR) && \
	sudo docker-compose exec -T web python manage.py compilemessages --no-input