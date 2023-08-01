# Используем официальный образ PostgreSQL из Docker Hub
FROM postgres:latest

# Копируем SQL-скрипт в папку инициализации
COPY init.sql /docker-entrypoint-initdb.d/

# Устанавливаем пароль для суперпользователя
ENV POSTGRES_PASSWORD mysecretpassword

# Задаем имя базы данных
ENV POSTGRES_DB quiz_database