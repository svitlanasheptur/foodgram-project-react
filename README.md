# Foodgram #

[![Foodgram Workflow](https://github.com/svitlanasheptur/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/svitlanasheptur/foodgram-project-react/actions/workflows/main.yml)

Проект Foodgram создан для любителей готовить, чтобы они могли публиковать свои рецепты и делиться ими с другими. Сервис Foodgram предоставляет платформу для обмена рецептами и изучения кулинарных идей других пользователей.

### Стек технологий ###

- Backend: Python, Django, Django REST Framework
- Frontend: React, HTML, CSS
- База данных: PostgreSQL
- Контейнеризация: Docker, Docker Compose
- CI/CD: GitHub Actions

## Как развернуть проект ##

Клонируйте репозиторий:

```
git clone https://github.com/yandex-praktikum/foodgram-project-react
```
Перейдите в директорию проекта:

```
cd foodgram-project-react
```

Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполните миграции:

```
python3 manage.py migrate
```

Запустите проект:

```
python3 manage.py runserver
```

Создайте файл .env в корневой директории проекта и заполните его следующими переменными:

- DB_HOST=db
- DB_PORT=5432

- POSTGRES_DB=имя_базы_данных
- POSTGRES_USER=имя_пользователя
- POSTGRES_PASSWORD=пароль

- DEBUG=False
- ALLOWED_HOSTS=имя_вашего_сайта

Запустите проект с помощью Docker Compose:

```
docker-compose up -d --build
```

Выполнение миграций и сбор статических файлов:

```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

Запустите Docker Compose на сервере:

```
scp -i path_to_SSH/SSH_name docker-compose.production.yml \
    username@server_ip:/home/username/taski/docker-compose.production.yml
```

Запустите Docker Compose в режиме демона:

```
sudo docker compose -f docker-compose.production.yml up -d
```

Выполните миграции, соберите статические файлы:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

Создайте суперпользователя:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

Перейдите по ссылке:

```
http://localhost:9000/admin/
```

Добавьте необходимые теги:

```
http://localhost:9000/admin/recipes/tag/add/
```

Импортируйте ингридиенты в формате json:

```
http://localhost:9000/admin/recipes/ingredient/import/
```

Обновите конфиг Nginx и перезагрузите его.

Страница проекта: https://lovefood.zapto.org/
Документация API: https://lovefood.zapto.org/api/

### Автор ###
Проект разработан Светланой Шептур
