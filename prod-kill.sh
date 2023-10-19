#!/bin/bash
cp env/prod/.env .env
docker compose -p cinema-prod down

rm .env
