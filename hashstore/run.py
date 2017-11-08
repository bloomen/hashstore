from flask import Flask, request
from flask.ext.api import status
app = Flask(__name__)


BR = "bad request", status.HTTP_400_BAD_REQUEST
NIL = "None"

store = {}


def get_store():
    global store
    return store


def log(func):
    print(func + ": " + str(dict(request.args)))


@app.route("/clear")
def clear():
    log('clear')
    s = get_store()
    size = len(s)
    del s
    s = {}
    return str(size), status.HTTP_200_OK


@app.route("/size")
def size():
    log('size')
    return str(len(get_store())), status.HTTP_200_OK


@app.route("/get")
def get():
    log('get')
    key = request.args.get('key')
    index = request.args.get('index')
    if key is None and index is None:
        return BR
    s = get_store()
    if key is not None:
        value = s.get(key)
        if value is None:
            return NIL, status.HTTP_204_NO_CONTENT
        else:
            return value, status.HTTP_200_OK
    if index is not None:
        try:
            ind = int(index)
        except:
            return BR
        i = 0 
        for k, _ in s.items():
            if i == ind:
                return k, status.HTTP_200_OK
            i += 1
        return NIL, status.HTTP_204_NO_CONTENT


@app.route("/put")
def put():
    log('put')
    key = request.args.get('key')
    value = request.args.get('value')
    if key is None or value is None:
        return BR
    s = get_store()
    old_value = s.get(key)
    s[key] = value
    if old_value is None:
        return NIL, status.HTTP_200_OK
    else:
        return old_value, status.HTTP_205_RESET_CONTENT


@app.route("/remove")
def remove():
    log('remove')
    key = request.args.get('key')
    if key is None:
        return BR
    s = get_store()
    old_value = s.get(key)
    if old_value is None:
        return NIL, status.HTTP_204_NO_CONTENT
    else:
        del s[key]
        return old_value, status.HTTP_200_OK
