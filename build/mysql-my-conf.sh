#!/usr/bin/env bash

USER=$1
PASS=$2

BLOCK="
[client]
user=$USER
password=$PASS

[mysql]
user=$USER
password=$PASS

[mysqldump]
user=$USER
password=$PASS

[mysqldiff]
user=$USER
password=$PASS
"

if [[ -n ${USER} && -n ${PASS} ]]; then
    echo "$BLOCK" > ~/.my.cnf
    chmod 600 ~/.my.cnf

    echo "User my.cnf has been created!"
else
    echo "Incorrect user or password. User my.cnf was not created"
    exit 1
fi