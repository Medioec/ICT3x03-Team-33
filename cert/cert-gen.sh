#!/bin/bash

mkdir -p ca
openssl genpkey -algorithm RSA -out ca/ca-key.pem
openssl req -new -x509 -key ca/ca-key.pem -out ca/ca-cert.pem -days 3650 -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Hackers/CN=EricCA"
mkdir -p certificates
sign_domain_cert() {
    domain=$1
    openssl genpkey -algorithm RSA -out certificates/$domain-key.pem
    openssl req -new -key certificates/$domain-key.pem -out certificates/$domain-csr.pem -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Hackers/CN=$domain"
    openssl x509 -req -in certificates/$domain-csr.pem -CA ca/ca-cert.pem -CAkey ca/ca-key.pem -CAcreateserial -out certificates/$domain-cert.pem -days 365
}

domains=(
    "frontend"
    "identity"
    "booking"
    "movie"
    "payment"
    "databaseservice"
    "nginx-waf"
    )

export OPENSSL_CONF="/dev/null"

for domain in "${domains[@]}"; do
    sign_domain_cert $domain
done

echo "Certificates generated successfully."
