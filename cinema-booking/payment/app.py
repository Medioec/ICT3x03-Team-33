from flask import Flask
from flask_cors import CORS
app = Flask(__name__)  
CORS(app)

@app.route('/')
def hello_geek():
    print("Hello from Payment Service")
    return '<h1>Hello from Payment Service</h2>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8084)
