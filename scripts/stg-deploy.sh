#!/bin/bash
# run this script from base repository directory
cp env/stg/.env .env
docker compose -p cinema-stg -f secure-compose.yml down --volumes
docker compose -p cinema-stg -f secure-compose.yml up -d --force-recreate

rm .env
