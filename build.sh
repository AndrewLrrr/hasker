#!/usr/bin/env bash

PROJECT_NAME=$1

while [[ -z ${PROJECT_NAME} ]]; do
    read -p "Enter project name: " PROJECT_NAME
done

PROJECT_PATH=$(pwd)/${PROJECT_NAME}
SECRET_KEY="$(openssl rand -base64 50)"
CONFIG=config.settings.production
DB_USER=hasker
DB_USER_PASS=Hasker1234
DB_ROOT_TMP_PASS=Root1234

echo "Try to update/upgrade repositories..."
apt-get -qq -y update
apt-get -qq -y upgrade

echo "Try to install Python2 with project dependencies..."
apt-get install -qq -y python python-pip
pip install --upgrade pip
pip install -r requirements.txt

echo "Try to install Mysql and create database..."
build-scripts/mysql-install.sh ${DB_ROOT_TMP_PASS}
service mysql start
build-scripts/mysql-my-conf.sh root ${DB_ROOT_TMP_PASS}
build-scripts/mysql-db.sh ${DB_USER} ${DB_USER_PASS}
apt-get install -y libmysqlclient-dev

echo "Try to install Nginx and create config..."
apt-get install -y nginx
service mysql start
build-scripts/nginx-conf.sh ${PROJECT_NAME}

echo "Try to install and configure Uwsgi daemon..."
pip install uwsgi
build-scripts/uwsgi-ini.sh ${PROJECT_NAME} ${PROJECT_PATH} ${CONFIG} ${DB_USER} ${DB_USER_PASS} ${SECRET_KEY}
# Looks like Docker has some problems with systemd...
# build-scripts/uwsgi-env.sh ${PROJECT_NAME} ${CONFIG} ${SECRET_KEY} ${DB_USER} ${DB_USER_PASS}
# build-scripts/uwsgi-service.sh ${PROJECT_NAME}

echo "Try to collect static and run migrations..."
cd ${PROJECT_PATH}
pip install mysql-python

DJANGO_SETTINGS_MODULE=${CONFIG} \
SECRET_KEY=${SECRET_KEY} \
python manage.py collectstatic

DJANGO_SETTINGS_MODULE=${CONFIG} \
SECRET_KEY=${SECRET_KEY} \
DATABASE_NAME=${DB_USER} \
DATABASE_USER=${DB_USER} \
DATABASE_PASSWORD=${DB_USER_PASS} \
python manage.py migrate

# systemctl start ${PROJECT_NAME}
uwsgi --ini /usr/local/etc/${PROJECT_NAME}.ini &