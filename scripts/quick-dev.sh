#!/bin/sh
./scripts/dev-build.sh && ./scripts/dev-deploy.sh && docker compose -p cinema-dev logs -f
