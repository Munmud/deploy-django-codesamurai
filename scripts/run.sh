#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py start_periodic_tasks
python manage.py load_initial_waste_db
python manage.py load_initial_auth_db

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
