#!/bin/bash
set -e
echo python3 manage.py makemigrations
python3 manage.py makemigrations
echo python3 manage.py migrate
python3 manage.py migrate
echo python3 manage.py runserver
python3 manage.py runserver 0.0.0.0:8000
