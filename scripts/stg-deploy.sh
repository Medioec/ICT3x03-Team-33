#!/bin/bash
# run this script from base repository directory
cp env/stg/.env .env
docker compose -p cinema-stg up -d --force-recreate

rm .env
