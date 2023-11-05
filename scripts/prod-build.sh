#!/bin/bash
# run this script from base repository directory
cp env/prod/.env .env
docker compose -p cinema-prod -f secure-compose.yml build
status=$?
rm .env
exit=$status
