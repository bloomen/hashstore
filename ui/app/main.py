from flask import Flask, request
from flask.templating import render_template
import requests

app = Flask(__name__)


def req(modifier, params):
    r = requests.get("http://127.0.0.1:5001/" + modifier, params=params)
    return r.text, r.status_code


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/clear")
def clear():
    return req("clear", request.args)


@app.route("/size")
def size():
    return req("size", request.args)


@app.route("/get")
def get():
    return req("get", request.args)


@app.route("/put")
def put():
    return req("put", request.args)


@app.route("/remove")
def remove():
    return req("remove", request.args)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
