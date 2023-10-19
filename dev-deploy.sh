#!/bin/bash
cp env/dev/.env .env
docker compose -p cinema-dev up -d
docker compose -p cinema-dev restart

rm .env
