#!/usr/bin/env bash

PROJECT_NAME=$1
DB_NAME=$2
DB_PASSWORD=$3

SECRET_KEY="$(openssl rand -base64 50)"

BLOCK="
SECRET_KEY=${SECRET_KEY}
DATABASE_NAME=${DB_NAME}
DATABASE_USER=${DB_NAME}
DATABASE_PASSWORD=${DB_PASSWORD}
"

if [[ -n ${DB_NAME} && -n ${DB_PASSWORD} && -n ${PROJECT_NAME} ]]; then
    echo "$BLOCK" > "/usr/local/etc/.env.${PROJECT_NAME}"
    systemctl start myproject
    echo "Uwsgi environment file has been created and started"
else
    echo "Incorrect environments data. Uwsgi environment file was not created"
    exit 1
fi