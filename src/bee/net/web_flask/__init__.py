#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

__author__ = 'wenchao.hao'

"""
net.web_flask package. use flask lib as bee's web framework
"""
app = Flask(__name__.split(".")[0])


@app.route('/', methods=['GET', 'POST'])
def home():
    s = '<h1>Welcome To Bee Web Home</h1>'
    s += "\n"
    s += "Use Native Flask Framework, enjoy it!"
    return s
