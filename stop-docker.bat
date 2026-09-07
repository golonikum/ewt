@echo off
echo Остановка Docker контейнеров...
docker-compose down -v

echo Docker контейнеры успешно остановлены и удалены
