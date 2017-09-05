#!/usr/bin/env bash

PROJECT_NAME=$1

BLOCK="
[Unit]
Description=$PROJECT_NAME uWSGI daemon

[Service]
EnvironmentFile=-/usr/local/etc/.env.$PROJECT_NAME
ExecStart=/usr/bin/bash -c 'uwsgi --ini /usr/local/etc/$PROJECT_NAME.ini'

[Install]
WantedBy=multi-user.target
"

if [[ -n ${PROJECT_NAME} ]]; then
    echo "$BLOCK" > "/etc/systemd/system/$PROJECT_NAME.service"
    systemctl start ${PROJECT_NAME}
    echo "Uwsgi service has been created and started"
else
    echo "Incorrect project name. Uwsgi service was not created"
    exit 1
fi