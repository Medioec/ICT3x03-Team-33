#!/bin/bash
# sets environment variables from a file
set -a
source $1
set +a
# sets non-persistent secrets
export JWT_SECRET_KEY=$(openssl rand -hex 32)
