# Размести свои рецепты здесь! (praktikum_diplom)

![example workflow](https://github.com/V1cimus/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Описание
Проект предназначен для Публикации рецептов. Кроме того вы можете добавлять рецепты в избранное, фильтровать их то тегам, подписываться на авторов и формировать собственный список покупок на основании рецептов добавленных в него. 

## Локальный запуск Backend.
Для локального запуска приложения создайте файл .env в корне backend/.env, пример расположен в директорию /infra/.

После создания файла выполните следующие команды.

```bash
python manage.py migrate
```

Наполните базу данных тестовыми данными.

```bash
python manage.py loaddata data/test_db_data.json
```

Создайте суперпользователя

```bash
python manage.py createsuperuser
```

Выполните команду для загрузки локализации, поддерживается русский и английский языки.

```bash
python manage.py compilemessages
```

Запустите сервер

```bash
python manage.py runserver
```

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

Выполните команду для загрузки локализации, поддерживается русский и английский языки.

```bash
sudo docker-compose exec web python manage.py compilemessages
```

Проект развернут и готов к работе!

Для получения информации о доступных командах перейдите в документацию к API по ссылке: 
- Docs: http://127.0.0.1/api/docs/;
- Swagger: http://127.0.0.1/api/swagger/.

### Остановка проекта

Выполните команду

```bash
docker-compose down -v
```

### Заполнение Базы Данных.

Создайте суперюзера.

```bash
winpty docker-compose exec web python manage.py createsuperuser
```

Заполните БД заранее подготовленными ингредиентами выполнив команду.

```bash
docker-compose exec web python manage.py load_csv_data
```

## Информация о боевом сервере в облаке.

Боевой сервер развернут при помощи YandexCloud.

Реализована технология автоматической загрузки изменений на сервер при помощи git action.
Создан пре-хук коммит для линтера ruff. 
Настроены файлы для диполя, такие как docker-compose.yml, nginx.conf, Makefile.

---
Неактуальная информация:

~~Адреса боевого сервера:~~ <br>
~~- http://vicimus-foodgram.sytes.net/;~~ <br>
~~- http://158.160.61.84/.~~ <br>

~~Документация доступна по следующим адресам:~~ <br>
~~- Docs: http://vicimus-foodgram.sytes.net/api/docs/;~~ <br>
~~- Swagger: http://vicimus-foodgram.sytes.net/api/swagger/.~~ <br>

~~Данные для входа под админом:~~ <br>
~~- Username: admin;~~ <br>
~~- Password: admin.~~ <br>
