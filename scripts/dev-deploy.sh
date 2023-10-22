#!/bin/bash
# run this script from base repository directory
cp env/dev/.env .env
docker compose -p cinema-dev up -d
docker compose -p cinema-dev restart

rm .env
