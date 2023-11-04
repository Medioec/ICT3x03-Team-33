#!/bin/bash
# sets environment variables from a file
readsecrets() {
    if [ -z $1 ]
    then
        set +x
        set -o allexport
        . $secrets_file
        export JWT_SECRET_KEY=$(openssl rand -hex 32)
        set +o allexport
        set -x
    else
        set +x
        set -o allexport
        . $1
        export JWT_SECRET_KEY=$(openssl rand -hex 32)
        set +o allexport
        set -x
    fi
}
readsecrets $1
