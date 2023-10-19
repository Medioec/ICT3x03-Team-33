#!/bin/bash
cp env/dev/.env .env
docker compose -p cinema-dev down

rm .env
