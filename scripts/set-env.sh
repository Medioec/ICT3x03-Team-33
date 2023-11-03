#!/bin/bash
# sets environment variables from a file
set -o allexport
readsecrets() {
    set +x
    . $secrets_file
    export JWT_SECRET_KEY=$(openssl rand -hex 32)
    set -x
}
readsecrets
set +o allexport
# sets non-persistent secrets

