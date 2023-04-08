PROJECT_NAME=foodgram
DOCKER_COMPOSE_FILE=infra/docker-compose.yml

all: 
up

up:
sudo docker-compose up -d

build:
sudo docker-compose build

restart:
sudo docker-compose restart

down:
sudo docker-compose down -v

clean:
sudo docker-compose down --rmi all --volumes --remove-orphans
