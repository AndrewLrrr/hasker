#!/usr/bin/env bash

DB_NAME=$1
DB_USER_PASS=$2

if [[ -n ${DB_NAME} && -n ${DB_USER_PASS} ]]; then
    # Удаляем БД и пользователя если они уже были созданы
    mysql -e "DROP DATABASE IF EXISTS $DB_NAME;"
    mysql -e "DROP USER IF EXISTS '$DB_NAME'@'localhost';"

    # Создаем новую БД на сервере
    mysql -e "CREATE DATABASE $DB_NAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
    # Создаем пользователя
    mysql -e "CREATE USER '$DB_NAME'@'localhost' IDENTIFIED BY '$DB_USER_PASS';"
    # Ограничиваем его права для общей БД
    mysql -e "GRANT USAGE ON *.* TO '$DB_NAME'@'localhost' IDENTIFIED BY '$DB_USER_PASS';"
    # Даем полные права для вновь созданной БД
    mysql -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_NAME'@'localhost';"

    echo "DB has been created!"
else
    echo "Incorrect database name or password. Database was not created"
    exit 1
fi