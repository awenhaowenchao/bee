from bee.net.web_flask import bapp
from bee.net.web_flask.server import start_up


@bapp.route('/hello', methods=['GET', 'POST'])
def hello():
    s = '<h1>Hello world</h1>'
    return s

start_up()