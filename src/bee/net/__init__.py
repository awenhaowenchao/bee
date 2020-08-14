#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wenchao.hao'

"""
net package. include rpc, web .. etc
"""

from bee.net.web_flask import bapp
from bee.net.web_flask.server import start_up as bapp_start_up

from .rpc.registry.registry import Server as RegistryServer
from .rpc.registry.consul_registry import ConsulRegistry
from .rpc.registry.etcdv3_registry import Etcd3Registry