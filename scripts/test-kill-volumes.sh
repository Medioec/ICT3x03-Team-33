#!/bin/bash
# run this script from base repository directory
cp env/test/.env .env
docker compose -p cinema-test down --volumes
status=$?
rm .env
exit=$status
