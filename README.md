# friends_service
Сервис друзей - тестовое задание на стажировку ВК

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=013220)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=013220)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=013220)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=013220)](https://www.docker.com/)

## Инструкция по развёртыванию:
1. Загрузите проект.
```
git clone https://github.com/felixffox/friends_service.git
```
2. Перейти в корневую директорию.
```
cd friends_service
```
3. Создать и активировать виртуальное окружение
```
python3 -m venv venv
source /venv/bin/activate (source /venv/Scripts/activate - для Windows)
python -m pip install --upgrade pip
```
4. Установить зависимости
```
pip install -r requirements.txt
```
5. Провести миграции и создать суперпользователя
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
6. Запустить сервер
```
python manage.py runserver
```

API проекта после запуска сервера будет доступно по адресу - http://127.0.0.1:8000/
В репозитории проекта так же подготовлен Dockerfile для возможности собрать проект в докер-образ

## Работа с API:
| Увидеть интерактивную спецификацию API вы сможете по адресу | `.../api/schema/swagger-ui/` | или | `.../api/schema/redoc/` |