#!/bin/bash
# run this script from base repository directory
if [ $1 != "test" ] && [ $1 != "dev" ] && [ $1 != "stg" ] && [ $1 != "prod" ]
then
    echo "Invalid env \"$1\" specified"
    exit 1
fi
echo "Environment: $1"
cp env/$1/.env .env
if [ $1 == "stg" ] || [ $1 == "prod" ]
then
    docker compose -p cinema-$1 -f secure-compose.yml build
else
    docker compose -p cinema-$1 build
fi
status=$?
rm .env
exit $status
