from typing import List

from bee.data.map import Map


class Option(Map):

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

def parse_option(s: str, sep: str) -> Option:
    pair = s.split(sep)
    return Option(name=pair[0], value=pair[1])



class Options(List[Option]):
    pass

def parse_options(s: str, sep1: str, sep2: str) -> Options:
    parts = s.split(sep1)
    opts = []
    for v in parts:
        opts.append(parse_option(v, sep2))
    return opts

