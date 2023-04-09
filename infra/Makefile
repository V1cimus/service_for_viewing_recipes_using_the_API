include .env

up:
	sudo docker pull ${DOCKER_USERNAME}/foodgram_backend:latest && \
	sudo docker-compose up -d && \
	sudo docker image prune -f

down:
	sudo docker-compose down -v

clean:
	sudo docker-compose down --rmi all --volumes --remove-orphans

rm_web:
	sudo docker-compose stop && \
	sudo docker image rm ${DOCKER_USERNAME}/foodgram_backend

migrate:
	sudo docker-compose exec -T web python manage.py migrate
    
collectstatic:
	sudo docker-compose exec -T web python manage.py collectstatic --no-input

localisation:
	sudo docker-compose exec -T web python manage.py compilemessages