# Gunicorn config variables
loglevel = "debug"
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
# ciphers = "ECDHE:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS:!RC4:!SHA"
# ssl_options = {
#     "ciphers": ciphers,
#     "server_side": True
# }
