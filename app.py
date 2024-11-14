from flask import Flask

from tcp_helper import run_server

app = Flask(__name__)


@app.route('/')
def hello_world():
    return run_server('localhost', 11000)


if __name__ == '__main__':
    # app.run(host='localhost', port=8080)
    run_server('localhost', 11000)
