DOCKER_COMPOSE_DIR := infra/

all: 
	cd $(DOCKER_COMPOSE_DIR)
	rm_web
	env
	up
	migrate
	collectstatic
	localisation

up:
	sudo docker pull ${{ secrets.DOCKER_USERNAME }}/api_yamdb:latest
	sudo docker-compose up -d
	sudo docker image prune -f

down:
	cd $(DOCKER_COMPOSE_DIR)
	sudo sudo docker-compose down -v

clean:
	cd $(DOCKER_COMPOSE_DIR)
	sudo docker-compose down --rmi all --volumes --remove-orphans

env:
	touch .env 
	echo DB_ENGINE=${{ secrets.DB_ENGINE }} > .env 
	echo DB_NAME=${{ secrets.DB_NAME }} >> .env 
	echo POSTGRES_USER=${{ secrets.POSTGRES_USER }} >> .env 
	echo POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }} >> .env 
	echo DB_HOST=${{ secrets.DB_HOST }} >> .env 
	echo DB_PORT=${{ secrets.DB_PORT }} >> .env
	echo DB_PORT=${{ secrets.DEBUG }} >> .env

rm_web:
	sudo docker-compose stop 
	sudo docker-compose rm web 

migrate:
	sudo docker-compose exec -T web python manage.py migrate
    
collectstatic:
	sudo docker-compose exec -T web python manage.py collectstatic --no-input

localisation:
	sudo docker-compose exec -T web python manage.py compilemessages
