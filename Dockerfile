# Используем официальный Python 2.7 образ
FROM python:2.7-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Debian buster вышел из поддержки — переключаемся на архивные репозитории
RUN sed -i 's|deb.debian.org/debian |archive.debian.org/debian |g; s|security.debian.org/debian-security|archive.debian.org/debian-security|g' /etc/apt/sources.list \
    && sed -i '/buster-updates/d' /etc/apt/sources.list \
    && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y     libpq-dev     gcc     python-dev     && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем директорию для медиа-файлов
RUN mkdir -p /app/media

# Устанавливаем переменные окружения
# DJANGO_SETTINGS_MODULE не задаём: manage.py сам выставляет "settings",
# т.к. проект использует settings/urls как модули верхнего уровня внутри djproject/
ENV PYTHONUNBUFFERED 1

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска задаётся в docker-compose.yml (gunicorn + nginx)
