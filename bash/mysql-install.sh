#!/usr/bin/env bash

TMP_PASS=$1

export DEBIAN_FRONTEND="noninteractive"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $TMP_PASS"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $TMP_PASS"
sudo apt-get install -y mysql-server-5.7