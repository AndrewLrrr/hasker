#!/usr/bin/env bash

CONFIG=$1
SECRET_KEY=$2
DB_NAME=$3
DB_PASSWORD=$4

if [[ -n ${DB_NAME} && -n ${DB_PASSWORD} && -n ${SECRET_KEY} ]]; then
    export DJANGO_SETTINGS_MODULE=${CONFIG}
    export SECRET_KEY=${SECRET_KEY}
    export DATABASE_NAME=${DB_NAME}
    export DATABASE_USER=${DB_NAME}
    export DATABASE_PASSWORD=${DB_PASSWORD}
else
    echo "Incorrect environments data. Environment variables were not created"
    exit 1
fi