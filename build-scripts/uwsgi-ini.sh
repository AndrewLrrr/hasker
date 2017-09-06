#!/usr/bin/env bash

PROJECT_NAME=$1
PROJECT_PATH=$2
CONFIG=$3
DB_NAME=$4
DB_PASSWORD=$5
SECRET_KEY=$6

BLOCK="
[uwsgi]
chdir=$PROJECT_PATH
module=config.wsgi:application
master = true
processes = 5
socket=/run/uwsgi/$PROJECT_NAME.sock
chmod-socket=666
logto = /var/log/$PROJECT_NAME.log
vacuum = true
die-on-term = true
env=DJANGO_SETTINGS_MODULE=${CONFIG}
env=SECRET_KEY=${SECRET_KEY}
env=DATABASE_NAME=${DB_NAME}
env=DATABASE_USER=${DB_NAME}
env=DATABASE_PASSWORD=${DB_PASSWORD}
"

if [[ -n ${PROJECT_NAME} && -n ${PROJECT_PATH} ]]; then
    if [[ ! -e /run/uwsgi ]]; then
        mkdir /run/uwsgi
    fi
    echo "$BLOCK" > "/usr/local/etc/$PROJECT_NAME.ini"
    echo "Uwsgi config has been created"
else
    echo "Incorrect project name or project path. Uwsgi config was not created"
    exit 1
fi