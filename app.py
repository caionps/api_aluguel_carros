from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def read():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['POST'])
def create():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['DELETE'])
def delete():
    return "<p>Hello, World!</p>"

@app.route('/', methods=['PUT'])
def update():
    return "<p>Hello, World!</p>"