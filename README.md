# FoodGram, размести свои рецепты здесь! (praktikum_diplom)

![example workflow](https://github.com/V1cimus/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/V1cimus/foodgram-project-react)

## Описание
Проект предназначен для Публикации рецептов. Кроме того вы можете добавлять рецепты в избранное, фильтровать их то тегам, подписываться на авторов и формировать собственный список покупок на основании рецептов добавленых в него. 


## Шаблон наполнения env-файла.
Для создания контейнера с БД необходимо поместить файл .env в директорию /infra/.env с наполнением соответствующем шаблону .env.example расположенным в той же директории.


## Запуск приложения в контейнерах.
Для запуска приложения запустите докер и выполните команду для создания образов и контейнеров находясь в директории с файлом docker-compose.yaml.

```bash
docker-compose up -d
```

Выполните миграции.

```bash
docker-compose exec web python manage.py migrate
```

Выполните команду для сбора статики.

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Проект развернут и готов к работе!

Для получения информации о доступных командах перейдите в документацию к API по ссылке http://127.0.0.1/api/docs/.


## Остановка проекта

Выполните команду

```bash
docker-compose down -v
```


## Заполнение Базы Данных.

Создайте суперюзера.

```bash
winpty docker-compose exec web python manage.py createsuperuser
```

Заполните БД заранее подготовленными ингредиентами выполнив команду.

```bash
docker-compose exec web python manage.py load_csv_data
```

ReadMe будет редактороваться по мере добавления проекта в облако.