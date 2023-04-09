DOCKER_COMPOSE_DIR := infra/

up:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker pull ${{ secrets.DOCKER_USERNAME }}/api_yamdb:latest
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose up -d
	cd $(DOCKER_COMPOSE_DIR) && sudo docker image prune -f

down:
	cd $(DOCKER_COMPOSE_DIR) && sudo sudo docker-compose down -v

clean:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose down --rmi all --volumes --remove-orphans

env:
	cd $(DOCKER_COMPOSE_DIR) && touch .env 
	cd $(DOCKER_COMPOSE_DIR) && echo DB_ENGINE=${{ secrets.DB_ENGINE }} > .env 
	cd $(DOCKER_COMPOSE_DIR) && echo DB_NAME=${{ secrets.DB_NAME }} >> .env 
	cd $(DOCKER_COMPOSE_DIR) && echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env 
	cd $(DOCKER_COMPOSE_DIR) && echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env 
	cd $(DOCKER_COMPOSE_DIR) && echo DB_HOST=${{ secrets.DB_HOST }} >> .env 
	cd $(DOCKER_COMPOSE_DIR) && echo DB_PORT=${{ secrets.DB_PORT }} >> .env
	cd $(DOCKER_COMPOSE_DIR) && echo DB_PORT=${{ secrets.DEBUG }} >> .env

rm_web:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose stop 
	cd $(DOCKER_COMPOSE_DIR) && sudo docker image rm vicimus/foodgram_backend

migrate:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose exec -T web python manage.py migrate
    
collectstatic:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose exec -T web python manage.py collectstatic --no-input

localisation:
	cd $(DOCKER_COMPOSE_DIR) && sudo docker-compose exec -T web python manage.py compilemessages
