#!/bin/sh
flask --app health run &
exec /docker-entrypoint.sh nginx -g "daemon off;"
