#!/usr/bin/env bash

SOURCE_PATH=~/hasker
DB_ROOT_TMP_PASS=Root1234
DB_NAME=hasker
DB_USER_PASS=Hasker1234

# Устанавливаем Nginx и Python
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y nginx python-minimal python-virtualenv python-pip
pip install --upgrade pip

# Устанавливаем БД
./mysql-install.sh ${DB_ROOT_TMP_PASS}
./create-my-conf.sh root ${DB_ROOT_TMP_PASS}
./create-db.sh ${DB_NAME} ${DB_USER_PASS}
sudo apt-get install -y libmysqlclient-dev

# Разворачиваем виртуальное окружение
cd ${SOURCE_PATH}
virtualenv virtenv
source virtenv/bin/activate
pip install uwsgi
pip install django

# Запускаем демонов
sudo systemctl restart nginx
sudo systemctl enable nginx
