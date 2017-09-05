#!/usr/bin/env bash

PROJECT_NAME=hasker

PROJECT_PATH=$(cd ~/${PROJECT_NAME}; pwd)

echo "Try to update/upgrade repositories..."
apt-get -qq -y update
apt-get -qq -y upgrade

echo "Try to install Python2 with project dependencies..."
apt-get install -qq -y python python-pip
pip install --upgrade pip
pip install -r requirements.txt

echo "Try to install Mysql and create database..."
DB_USER=hasker
DB_USER_PASS=Hasker1234
DB_ROOT_TMP_PASS=Root1234
mysql-install.sh ${DB_ROOT_TMP_PASS}
mysql-my-conf.sh root ${DB_ROOT_TMP_PASS}
mysql-db.sh ${DB_USER} ${DB_USER_PASS}
apt-get install -y libmysqlclient-dev

echo "Try to install Nginx and create config..."
apt-get install -y nginx
nginx-conf.sh ${PROJECT_NAME}

echo "Try to collect static and run migrations..."
cd ${PROJECT_PATH}
python manage.py collectstatic
python manage.py migrate

echo "Try to install and configure Uwsgi daemon..."
SECRET_KEY="$(openssl rand -base64 50)"
pip install uwsgi
uwsgi-ini.sh ${PROJECT_NAME} ${PROJECT_PATH}
uwsgi-env.sh ${PROJECT_NAME} ${DB_USER} ${DB_USER_PASS}
uwsgi-service.sh ${PROJECT_NAME}