#!/usr/bin/env bash

PROJECT_NAME=$1
CONFIG=$2
SECRET_KEY=$3
DB_NAME=$4
DB_PASSWORD=$5

BLOCK="
DJANGO_SETTINGS_MODULE=${CONFIG}
SECRET_KEY=${SECRET_KEY}
DATABASE_NAME=${DB_NAME}
DATABASE_USER=${DB_NAME}
DATABASE_PASSWORD=${DB_PASSWORD}
"

if [[ -n ${DB_NAME} && -n ${DB_PASSWORD} && -n ${PROJECT_NAME} && -n ${SECRET_KEY} && -n ${CONFIG} ]]; then
    echo "$BLOCK" > "/usr/local/etc/.env.${PROJECT_NAME}"
    echo "Uwsgi environment file has been created"
else
    echo "Incorrect environments data. Uwsgi environment file was not created"
    exit 1
fi