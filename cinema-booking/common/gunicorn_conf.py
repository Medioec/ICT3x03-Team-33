# Gunicorn config variables
loglevel = "info"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = 120
timeout = 120
keepalive = 5
threads = 3
bind = "0.0.0.0:443"
keyfile = "privkey.pem"
certfile = "fullchain.pem"
ca_certs = "ca-cert.pem"
ssl_version = 2
cert_reqs = 2
preload = True
ciphers = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
ssl_options = {
    "ciphers": ciphers,
    "server_side": True
}
