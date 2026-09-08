# Django 6.1 поддерживает Python 3.12, 3.13 и 3.14
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости.
# Все пакеты ставятся из готовых wheel, поэтому компилятор и apt не нужны:
# psycopg[binary] содержит собранный libpq.
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

# Команда по умолчанию. docker-compose.yml задаёт её же явно, но без CMD
# образ наследует от базового образа запуск интерпретатора, который
# без TTY сразу получает EOF и завершается — платформы, запускающие образ
# напрямую (render.com, northflank), видят это как "Application exited early".
CMD ["python", "djproject/docker_start.py"]
