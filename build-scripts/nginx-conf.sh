#!/usr/bin/env bash

PROJECT_NAME=$1
DOMAIN=$2

if [[ -z ${DOMAIN} ]]; then
    DOMAIN="localhost 127.0.0.1"
    if [[ -f /etc/nginx/sites-available/default ]]; then
        rm /etc/nginx/sites-available/default
    fi
    if [[ -h /etc/nginx/sites-enabled/default ]]; then
        rm /etc/nginx/sites-enabled/default
    fi
fi

BLOCK="
upstream $PROJECT_NAME {
    server 127.0.0.1:9999;
}
server {
    listen       80;
    server_name  $DOMAIN;

    charset utf-8;

    access_log /var/log/nginx/$PROJECT_NAME-access.log combined;
    error_log  /var/log/nginx/$PROJECT_NAME-error.log error;

    location /static/ {
        root /var/www/$PROJECT_NAME;
    }

    location /media/ {
        root /var/www/$PROJECT_NAME;
    }

    location / {
        include    uwsgi_params;
        uwsgi_pass $PROJECT_NAME;
    }
}
"

if [[ -n ${PROJECT_NAME} ]]; then
    if [[ -f /etc/nginx/sites-available/${PROJECT_NAME} ]]; then
        rm /etc/nginx/sites-available/${PROJECT_NAME}
    fi

    if [[ -h /etc/nginx/sites-enabled/${PROJECT_NAME} ]]; then
        rm /etc/nginx/sites-enabled/${PROJECT_NAME}
    fi

    echo "$BLOCK" > "/etc/nginx/sites-available/$PROJECT_NAME"
    ln -fs "/etc/nginx/sites-available/$PROJECT_NAME" "/etc/nginx/sites-enabled/$PROJECT_NAME"
    service nginx reload
    echo "Nginx config has been created"
else
    echo "Incorrect project name. Nginx config was not created"
    exit 1
fi