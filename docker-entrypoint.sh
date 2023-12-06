#!/bin/bash

# Apply database migrations
poetry run python manage.py migrate --noinput || exit 1

# Start the Django development server
poetry run python manage.py runserver 0.0.0.0:8000

exec "$@"