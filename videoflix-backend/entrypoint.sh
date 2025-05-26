#!/bin/sh

echo "Warte auf Datenbank..."

# Warte, bis PostgreSQL erreichbar ist
until nc -z db 5432; do
  sleep 1
done

echo "Datenbank ist verfügbar"

# Migration & Static-Files
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
