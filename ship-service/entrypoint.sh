#!/bin/sh
set -e
echo "Running migrations..."
python manage.py makemigrations app --noinput 2>/dev/null || true
python manage.py makemigrations --noinput 2>/dev/null || true
python manage.py migrate --noinput
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
