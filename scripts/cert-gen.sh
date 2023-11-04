#!/bin/bash

certdir='cert/certificates'
cadir='cert/ca'

mkdir -p $cadir
#openssl genpkey -algorithm RSA -out $cadir/ca-key.pem
openssl ecparam -genkey -name secp384r1 -out $cadir/ca-key.pem
#openssl req -new -x509 -key $cadir/ca-key.pem -out $cadir/ca-cert.pem -days 3650 -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Hackers/CN=EricCA"
openssl req -new -x509 -SHA384 -nodes -key $cadir/ca-key.pem -out $cadir/ca-cert.pem -days 3650 -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Pomudachi/CN=EricCA"
mkdir -p $certdir
sign_domain_cert() {
    domain=$1
    #openssl genpkey -algorithm RSA -out $certdir/$domain-key.pem
    openssl ecparam -genkey -name secp384r1 -out $certdir/$domain-key.pem
    #openssl req -new -key $certdir/$domain-key.pem -out $certdir/$domain-csr.pem -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Hackers/CN=$domain" -reqexts SAN -extensions SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:$domain"))
    openssl req -new -SHA384 -nodes -key $certdir/$domain-key.pem -out $certdir/$domain-csr.pem -subj "/C=SG/ST=SG/L=SG/O=3x03/OU=Pomudachi/CN=$domain" -reqexts SAN -extensions SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:$domain"))
    openssl x509 -req -SHA384 -extfile v3.ext -in $certdir/$domain-csr.pem -CA $cadir/ca-cert.pem -CAkey $cadir/ca-key.pem -CAcreateserial -out $certdir/$domain-cert.pem -days 365 -extensions SAN -extfile <(cat /etc/ssl/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:$domain"))
}

domains=(
    "frontend"
    "identity"
    "booking"
    "movie"
    "payment"
    "databaseservice"
    "nginx-waf"
    "email"
    )

for domain in "${domains[@]}"; do
    sign_domain_cert $domain
done

echo "Certificates generated successfully."
