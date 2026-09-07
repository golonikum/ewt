@echo off
chcp 65001 >nul

echo Создание .env файла, если он не существует...
if not exist ".env" (
    echo Создание .env файла...
    copy ".env.example" ".env"
    echo Пожалуйста, отредактируйте .env файл с вашими настройками
)

echo Остановка и удаление предыдущих контейнеров...
docker-compose down -v

echo Сборка Docker образов...
docker-compose build

echo Запуск Docker контейнеров...
docker-compose up -d

echo Ожидание запуска базы данных...
:loop
docker-compose exec db pg_isready -U etrainer_golonru -d etrainer_golonru > nul 2>&1
if %errorlevel% neq 0 (
    echo База данных недоступна - ожидание...
    timeout /t 1 /nobreak > nul
    goto loop
)
echo База данных готова

echo Применение схемы БД (Django 1.4: syncdb)...
docker-compose exec -w /app/djproject web python manage.py syncdb --noinput

echo Загрузка начальных данных...
docker-compose exec -w /app/djproject web python manage.py loaddata core/fixtures/initial_data.json

echo Приложение успешно запущено!
echo Откройте браузер и перейдите по адресу: http://localhost:8000
echo.
echo Для просмотра логов используйте: docker-compose logs -f
echo Для остановки контейнеров используйте: stop-docker.bat
