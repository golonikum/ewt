# Используем официальный Python 2.7 образ
FROM python:2.7-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости.
# Все пакеты ставятся из готовых wheel, поэтому компилятор и apt не нужны:
# базовый образ основан на Debian buster, чьи репозитории уехали в архив
# и при сборке на чужой машине периодически недоступны.
#
# Django 1.4 старше формата wheel, и его setup.py при попытке сборки печатает
# "Django 1.4 does not support wheel. This error is safe to ignore." —
# pip действительно игнорирует это и ставит пакет через setup.py install.
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
