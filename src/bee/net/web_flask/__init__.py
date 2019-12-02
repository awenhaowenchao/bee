#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from bee import config
from bee.data.guid import Guid
from bee.data.map import Map
from bee.bee import banner

__author__ = 'wenchao.hao'

"""
net.web_flask package. use flask lib as bee's web framework
"""
app = Flask(__name__.split(".")[0])
bapp = Blueprint('bee-' + Guid().string(), __name__)
print(bapp.name)


@bapp.route('/', methods=['GET', 'POST'])
def home():
    s = '<h1>Welcome To Bee Web Home</h1>'
    s += "\n"
    s += "Use Natural Flask Framework, enjoy it!"
    return s


class ServerOptions(Map):

    def __init__(self, port: int = 8080, context_path: str = "bee", banner: bool = True, debug: bool = True):
        self.port = port
        self.path = context_path
        self.banner = banner
        self.debug = debug


def start():
    port = config.get("server.port")
    path = config.get("server.context-path")
    opts = ServerOptions(port=port, context_path=path)
    if opts.debug:
        print(banner)

    app.register_blueprint(bapp, url_prefix=path)
    app.run(debug=opts.debug, use_reloader=False, host='0.0.0.0', port=port)
