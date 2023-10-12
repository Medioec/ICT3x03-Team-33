from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Database Service</h2>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
