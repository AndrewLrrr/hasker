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

sudo echo "$BLOCK" > ~/.my.cnf
sudo chmod 600 ~/.my.cnf