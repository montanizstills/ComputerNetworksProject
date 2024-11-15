from flask import Flask

from tcp_helper import run_server

app = Flask(__name__)


@app.route('/')
def hello_world():
    return """Hello, World!"""


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=1000)

