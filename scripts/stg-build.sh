#!/bin/bash
# run this script from base repository directory
cp env/stg/.env .env
docker compose -p cinema-stg -f secure-compose.yml build
status=$?
rm .env
exit=$status
