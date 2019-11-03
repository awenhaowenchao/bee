import json
import os

import yaml

from bee.data.map import Map
from bee.data.option import Option
from bee.errors.error import BeeError

class SourceTypeError(BeeError):
    pass

class Source():

    def load(self) -> Map:
        pass


# def merge_option(opts: Map, k: str, v):
#     keys = k.split(".")
#     new_keys = []
#     for value in keys:
#         if value != "":
#             new_keys.append(value)
#     keys = new_keys
#     length = len(keys)
#     last = length -1
#     for i in range(length):
#
#         key = keys[i]
#         if opts.contains(key):
#             opt = opts.get(key)
#             t = type(opt)
#             if t == Map:
#                 opts = opt
#             elif t == dict:
#                 opts = Map.from_dict(opt)
#             else:
#                 return
#         else:
#             if i == last:
#                 opts[key] = v
#             else:
#                 opts[key] = Map()


def merge_option(opts: Map, k: str, v):
    keys = k.split(".")
    new_keys = []
    for value in keys:
        if value != "":
            new_keys.append(value)
    keys = new_keys
    length = len(keys)
    last = length - 1
    if length > 1:
        for i in range(length):
            key = keys[i:i+1][0]
            if i < last:
                if opts.get(key) == None:
                    opts = opts.setdefault(key, Map())
                else:
                    opts = opts.get(key)
                    if opts.contains(keys[i+1:i+2][0]):
                        if i == last-1:
                            return
                        else:
                            t = type(opts.get(keys[i+1:i+2][0]))
                            if t!=Map and t!=dict:
                                return
            else:
                opts.setdefault(key, v)

    else:
        if opts.contains(k) == False:
            opts.set(k, v)

def cover_option(opts: Map, k: str, v):
    # print("opts=%s, k=%s, v=%s" % (opts, k, v))
    # keys = k.split(".")
    # length = len(keys)
    # last = length -1
    # for i in range(length):
    #     key = keys[i]
    #     if opts.contains(key):
    #         opt = opts.get(key)
    #         t = type(opt)
    #         if t == Map:
    #             pass
    #         elif t == map:
    #             pass
    #         else:
    #             return
    #     if i == last:
    #         opts[key] = v
    #     else:
    #         opts = opts.setdefault(key, Map())
    keys = k.split(".")
    new_keys = []
    for value in keys:
        if value != "":
            new_keys.append(value)
    keys = new_keys
    length = len(keys)
    last = length - 1
    if length > 1:
        for i in range(length):
            key = keys[i:i + 1][0]
            if i < last:
                if opts.get(key) == None:
                    opts = opts.setdefault(key, Map())
                else:
                    opts = opts.get(key)
                    print(opts)
            else:
                opts.setdefault(key, v)

    else:
        opts.set(k, v)

class FileSource(str):

    def load(self) -> Map :
        path = str(self)

        with open(path, "rb") as f:
            file_name = f.name
            last_dot_index = file_name.rfind(".")
            t = file_name[last_dot_index+1:]
            b = f.read()
            bds = ByteDataSource(d=b, t=t)
            return bds.load()

class EnvSource(Source):

    def __init__(self, prefix: str=None, aliases: Map=None):
        self.prefix = prefix
        self.aliases = aliases

    def load(self) -> Map :
        opts = Map()
        envs = os.environ
        for k, v in envs.items():
            opt = Option(name=k, value=v)
            key = opt.name.lower()
            if self.prefix != None and self.prefix != "":
                key = key.strip(self.prefix).lower()
            # key = opt.name.replace("_", ".").lower()
            # print("key=%s, value=%s" % (key, opt.value))
            merge_option(opts, key, opt.value)
        # print(opts)
        return opts

    def set_prefix(self, prefix: str=None):
        self.prefix = prefix

    def set_aliases(self, alias: str=None, key: str=None):
        if self.aliases == None:
            self.aliases = Map()
        self.aliases.set(alias, key)


def load_source(t: str, d: bytes) -> Map:
    if t == "yaml" or t == "yml":
        return Map.from_dict(d=yaml.load(d, Loader=yaml.FullLoader))
    elif t == "json":
        return Map.from_dict(d=json.loads(d))
    else:
        raise SourceTypeError("unsupported config type")


class ByteDataSource(Source):

    def __init__(self, d: bytes, t: str):
        self.data: bytes = d
        self.type: str = t

    def load(self) -> Map:
        return load_source(self.type, self.data)