from flask import Flask, request, abort
from flask_api import status
from hashstore.store import Store
app = Flask(__name__)

KEY = 'k'
VALUE = 'v'
INDEX = 'i'
NIL = ''

store = Store()


def get_store():
    global store
    return store


@app.route("/clear")
def clear():
    s = get_store()
    size = s.size()
    s.clear()
    return str(size), status.HTTP_200_OK


@app.route("/size")
def size():
    return str(get_store().size()), status.HTTP_200_OK


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
        k = s.key(ind)
        if k is not None:
            return k
        return NIL, status.HTTP_204_NO_CONTENT


@app.route("/put")
def put():
    key = request.args.get(KEY)
    value = request.args.get(VALUE)
    if key is None or value is None:
        abort(status.HTTP_400_BAD_REQUEST)
    s = get_store()
    old_value = s.get(key)
    s.put(key, value)
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
        s.remove(key)
        return old_value, status.HTTP_200_OK
