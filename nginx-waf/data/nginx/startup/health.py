from flask import Flask, request
from jsom import *

app = Flask(__name__)

@app.route('/health')
def check_health():
    param = request.args.get('check', '')
    if param == 'health':
        return 'healthy'
    else:
        return dumps(param)
