from .routes import app


if __name__ == '__main__':
    app.run('localhost', 5001, debug=True)
