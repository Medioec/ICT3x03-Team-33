from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Booking Service</h2>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8083)
