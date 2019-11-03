import os

from bee.config.manager import Manager

def init_mamager() -> Manager:
    m = Manager.new("app")
    m.add_folder("./samples")
    return m

def test_find_file():
    m = init_mamager()
    s = m.find_file("app", ".yml")
    print(s)

def test_find_files():
    m = init_mamager()
    s = m.find_files("app", ".yml", ".json")
    print(s)

def test_find_folder():
    m = init_mamager()
    s = m.find_folder("test2")
    print(s)

def test_find_folders():
    m = init_mamager()
    s = m.find_folders("test1")
    print(s)

def test_type():
    m = init_mamager()
    cases = [("yaml.name", "yaml"),
             ("json.name", "json")]

    for v in cases:
        tv = m.get(v[0])
        print(tv)

def test_get():
    m = init_mamager()
    m.add_folder(".")
    m.set_profiles("dev")
    print(m.get("test.id"))

def test_byte_source():
    m = init_mamager()
    m.add_byte_source(b"name: awen", "yaml")
    v = m.get("name")
    print(v)

def test_env():
    DB_ADDRESS_KEY = "db.address"
    DB_ADDRESS_ENV_KEY = "DB_ADDRESS"
    DB_ADDRESS = "127.0.0.1"

    os.environ.setdefault(DB_ADDRESS_ENV_KEY, DB_ADDRESS)
    os.environ.setdefault("A_B_C", "test")
    print(os.environ)

    m = init_mamager()
    m.set_env_prefix("")
    m.bind_env(DB_ADDRESS_KEY, DB_ADDRESS_ENV_KEY)

    cases = [(DB_ADDRESS_KEY, DB_ADDRESS_ENV_KEY),
             ("a.b.c", "test")]
    for v in cases:
        tv = m.get(v[0])
        print("v=%s, tv=%s" % (v[0], tv))

def test_set_default():
    DB_ADDRESS_KEY = "db.address"
    DB_ADDRESS_ENV_KEY = "DB_ADDRESS"
    DB_ADDRESS = "127.0.0.1"

    os.environ.setdefault(DB_ADDRESS_ENV_KEY, DB_ADDRESS)
    os.environ.setdefault("A_B_C", "test")

    m = init_mamager()
    m.set_env_prefix("")
    m.bind_env(DB_ADDRESS_KEY, DB_ADDRESS_ENV_KEY)
    m.set_default_value("a.b.C", "test1")
    print(m.get("a.b.c"))
    print(m.options)

test_find_file()
test_find_files()
test_find_folder()
test_find_folders()
test_type()
test_get()

test_byte_source()
test_env()
test_set_default()