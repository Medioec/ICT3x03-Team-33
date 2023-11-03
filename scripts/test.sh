#!/bin/bash
# run this script from base repository directory
if [ $1 != "test" ] && [ $1 != "dev" ] && [ $1 != "stg" ] && [ $1 != "prod" ];
then
    echo "Invalid env \"$1\" specified";
    exit 1;
fi
echo "Starting test on environment: $1"
cp env/$1/.env .env
docker compose -p cinema-$1 -f test-compose.yml run --rm ubuntu
status=$?
echo "Test completed with status: $status"
rm .env
exit $status
