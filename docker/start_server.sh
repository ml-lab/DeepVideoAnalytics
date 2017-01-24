#!/usr/bin/env bash
set -xe
chown -R rabbitmq:rabbitmq /data
rabbitmq-server -detached
sleep 30
rabbitmqctl add_user dvauser localpass
rabbitmqctl set_permissions -p "/" dvuser ".*" ".*" ".*"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('dvauser', 'dvauser@akshaybhat.com', 'localpass')" | python manage.py shell
python manage.py runserver 0.0.0.0:8000