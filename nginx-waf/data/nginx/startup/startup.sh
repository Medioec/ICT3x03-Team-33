#!/bin/bash
if [ -z "$HEALTH" ] || [ $HEALTH == true ]
then
    flask --app health run &
fi
exec /docker-entrypoint.sh nginx -g "daemon off;"
