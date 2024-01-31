#!/bin/bash

poetry run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput
poetry run python manage.py db_fixtures
poetry run python manage.py runserver 0.0.0.0:8000