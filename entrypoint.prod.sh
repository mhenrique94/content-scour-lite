#!/bin/bash

if [ "$DB_NAME" = "djangoec2" ]
then
  echo "Aguardando RDS postgreSQL..."

  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done

  echo "RDS PostgreSQL iniciado!"
fi

# 1. exec ./manage.py collectstatic --noinput
# 2. Apply database migrations
#exec python manage.py migrate

# 3. Initialize database with init.sql
#psql -d "djangoec2" -U "postgres" -f init.sql

# 4. Start Gunicorn server as foreground process
exec gunicorn contentscour.wsgi:application --bind 0.0.0.0:8000
