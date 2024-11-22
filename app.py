from crypt import methods

from flask import Flask

from tcp_helper import run_server

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return """Hello, World!"""


@app.route('/', methods=['POST'])
def user_clicks_send_button():
    # get data from HTML input field
    # take data and send to server
    pass


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=1000)

