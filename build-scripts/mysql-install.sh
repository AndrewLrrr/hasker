#!/usr/bin/env bash

TMP_PASS=$1

if [[ -n ${TMP_PASS} ]]; then
    export DEBIAN_FRONTEND="noninteractive"
    debconf-set-selections <<< "mysql-server mysql-server/root_password password $TMP_PASS"
    debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $TMP_PASS"
    apt-get install -qq -y mysql-server-5.7

    echo "Mysql has been installed!"
else
    echo "Incorrect temporary password. Mysql was not installed"
    exit 1
fi