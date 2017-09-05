#!/usr/bin/env bash

PROJECT_NAME=$1
PROJECT_PATH=$2

BLOCK="
[uwsgi]
chdir=$PROJECT_PATH
module=config.wsgi:application
module = ip2w:application
master = true
processes = 5
socket = 127.0.0.1:9999
logto = /var/log/$PROJECT_NAME.log
vacuum = true
die-on-term = true
env=DJANGO_SETTINGS_MODULE=config.settings.production
"

if [[ -n ${PROJECT_NAME} && -n ${PROJECT_PATH} ]]; then
    echo "$BLOCK" > "/usr/local/etc/$PROJECT_NAME.ini"
    echo "Uwsgi config has been created"
else
    echo "Incorrect project name or project path. Uwsgi config was not created"
    exit 1
fi