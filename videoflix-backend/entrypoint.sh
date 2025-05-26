#!/bin/sh

echo "Warte auf Datenbank..."

# Waiting for the database to be available
until nc -z db 5432; do
  sleep 1
done

echo "Datenbank ist verfügbar"

python manage.py migrate --noinput
python manage.py collectstatic --noinput


echo "check for superuser..."

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Kein Superuser gefunden, erstelle einen...')
    User.objects.create_superuser(
        username='${DJANGO_SUPERUSER_USERNAME:-admin}',
        email='${DJANGO_SUPERUSER_EMAIL:-admin@example.com}',
        password='${DJANGO_SUPERUSER_PASSWORD:-adminpass}'
    )
else:
    print('Superuser already exisits!')
"

exec "$@"
