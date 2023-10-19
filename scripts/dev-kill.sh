#!/bin/bash
# run this script from base repository directory
cp env/dev/.env .env
docker compose -p cinema-dev down

rm .env
