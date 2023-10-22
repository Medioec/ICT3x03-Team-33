@echo off
REM Run this script from the base repository directory
copy env\dev\.env .env
docker-compose -p cinema-dev down
del .env
