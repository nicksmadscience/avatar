from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello_world():
    print (request.data)
    return "<p>Hello, World!</p>"