from flask import Flask, request, abort
from flask_api import status
app = Flask(__name__)

KEY = 'k'
VALUE = 'v'
INDEX = 'i'
NIL = ''

store = {}


def get_store():
    global store
    return store


@app.route("/clear")
def clear():
    s = get_store()
    size = len(s)
    s.clear()
    return str(size), status.HTTP_200_OK


@app.route("/size")
def size():
    return str(len(get_store())), status.HTTP_200_OK


@app.route("/get")
def get():
    key = request.args.get(KEY)
    index = request.args.get(INDEX)
    if key is None and index is None:
        abort(status.HTTP_400_BAD_REQUEST)
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
        except ValueError:
            abort(status.HTTP_400_BAD_REQUEST)
        i = 0
        for k, _ in s.items():
            if i == ind:
                return k, status.HTTP_200_OK
            i += 1
        return NIL, status.HTTP_204_NO_CONTENT


@app.route("/put")
def put():
    key = request.args.get(KEY)
    value = request.args.get(VALUE)
    if key is None or value is None:
        abort(status.HTTP_400_BAD_REQUEST)
    s = get_store()
    old_value = s.get(key)
    s[key] = value
    if old_value is None:
        return NIL, status.HTTP_200_OK
    else:
        return old_value, status.HTTP_205_RESET_CONTENT


@app.route("/remove")
def remove():
    key = request.args.get(KEY)
    if key is None:
        abort(status.HTTP_400_BAD_REQUEST)
    s = get_store()
    old_value = s.get(key)
    if old_value is None:
        return NIL, status.HTTP_204_NO_CONTENT
    else:
        del s[key]
        return old_value, status.HTTP_200_OK
