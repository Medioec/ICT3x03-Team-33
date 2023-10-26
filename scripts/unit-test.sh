#!/bin/bash
# run this script from base repository directory
cp env/test/.env .env
docker compose -p cinema-test -f test-compose.yml run --rm ubuntu
status=$?
rm .env
exit $status
