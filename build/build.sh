#!/usr/bin/env bash

PROJECT_NAME=hasker

if [[ ! -e ~/${PROJECT_NAME} ]]; then
    mkdir ~/${PROJECT_NAME}
elif [[ ! -d ~/${PROJECT_NAME} ]]; then
    echo "~/$PROJECT_NAME already exists but is not a directory" 1>&2
fi

PROJECT_PATH=$(cd ~/${PROJECT_NAME}; pwd)

echo "Try to update/upgrade repositories..."
apt-get -qq -y update
apt-get -qq -y upgrade

# Устанавливаем Python с зависимостями
echo "Try to install python2 with project dependencies..."
apt-get install -qq -y python python-pip
pip install --upgrade pip
cd ${PROJECT_PATH}
pip install -r requirements.txt

# Устанавливаем БД
echo "Try to install Mysql and create database..."
DB_USER=hasker
DB_USER_PASS=Hasker1234
DB_ROOT_TMP_PASS=Root1234
./mysql-install.sh ${DB_ROOT_TMP_PASS}
./mysql-my-conf.sh root ${DB_ROOT_TMP_PASS}
./mysql-db.sh ${DB_USER} ${DB_USER_PASS}
apt-get install -y libmysqlclient-dev

# Устанавливаем и конфигурируем nginx
echo "Try to install Nginx and create config..."
apt-get install -y nginx
./nginx-conf.sh ${PROJECT_NAME}

# Устанавливаем и конфигурируем uwsgi
echo "Try to install and configure Uwsgi daemon..."
SECRET_KEY="$(openssl rand -base64 50)"
pip install uwsgi
./uwsgi-ini.sh ${PROJECT_NAME} ${PROJECT_PATH}
cat > "/usr/local/etc/.env_${PROJECT_NAME}" << EOF
SECRET_KEY=${SECRET_KEY}
DATABASE_NAME=${DB_NAME}
DATABASE_USER=${DB_USER}
DATABASE_PASSWORD=${DB_PASSWORD}
EOF
sudo systemctl start ${PROJECT_NAME}
