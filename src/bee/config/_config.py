from typing import List

from bee.config.manager import Manager

m = Manager.new("app")

def find_file(name: str, *exts) -> str :
    return m.find_file(name, exts)

def find_files(name: str, *exts) -> List[str]:
    return m.find_files(name, exts)

def find_folder(name: str) -> str:
    return m.find_folder(name)

def find_folders(name: str) -> List[str]:
    return m.find_folders(name)

def set_env_prefix(prefix: str):
    m.set_env_prefix(prefix)

def set_profiles(*profiles: str):
    m.set_profiles(profiles)

def bind_env(key: str, env_key: str):
    m.bind_env(key, env_key)

def set_name(name: str):
    m.set_name(name)

def add_folder(*dirs: str):
    m.add_folder(dirs)

def add_source(*srcs):
    m.add_source(srcs)

def add_byte_source(d: bytes, t: str):
    m.add_byte_source(d, t)

def set_default_value(name: str, value):
    m.set_default_value(name, value)

def load():
    m.load(True)

def exist(key: str) -> bool:
    return m.get(key) != None

def get(key: str) -> object:
    return m.get(key)