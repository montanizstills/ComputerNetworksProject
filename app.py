from flask import Flask

from tcp_helper import run_server

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Hello, World!"""


if __name__ == '__main__':
    app.run(host='localhost', port=9688)
    # run_server('0.0.0.0', 11000)
