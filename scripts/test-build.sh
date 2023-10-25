#!/bin/bash
# run this script from base repository directory
cp env/test/.env .env
docker compose -p cinema-test build
status=$?
rm .env
exit=$status
