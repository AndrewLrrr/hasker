#!/usr/bin/env bash

PROJECT_PATH=$(cd ~/hasker; pwd)

# Устанавливаем Python с глобальными зависимостями
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get install -y python-minimal python-virtualenv python-pip
pip install --upgrade pip
pip install uwsgi

# Устанавливаем БД
DB_USER=hasker
DB_USER_PASS=Hasker1234
DB_ROOT_TMP_PASS=Root1234
./mysql-install.sh ${DB_ROOT_TMP_PASS}
./mysql-my-conf.sh root ${DB_ROOT_TMP_PASS}
./mysql-db.sh ${DB_USER} ${DB_USER_PASS}
sudo apt-get install -y libmysqlclient-dev

# Разворачиваем виртуальное окружение
cd ${PROJECT_PATH}
virtualenv virtenv
source virtenv/bin/activate
pip install -r requirements.txt
# ...

# Устанавливаем nginx
sudo apt-get install -y nginx
# ...
sudo systemctl restart nginx
sudo systemctl enable nginx

