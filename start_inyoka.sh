#!/bin/bash
cd /srv/www/inyoka
source ~/.venvs/inyoka/bin/activate
python manage.py migrate
python manage.py create_superuser --username admin --password $INYOKA_ADMIN_PASSWORD --email 'admin@localhost' || true 
./make_testdata.py || true
python manage.py runserver 0.0.0.0:8080

