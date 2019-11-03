from typing import List

import yaml

from bee import config
from bee.data.map import Map
from bee.ext import files


class ITranslator():

    def get(self, key: str):
        pass

    def format(self, key: str, *args: str) -> str:
        pass

class Translator():

    def __init__(self, lang: str, m: Map):
        self.lang = lang
        self._m = m

    def get(self, key: str):
        return self._m.find(key)

    def format(self, key: str, *args: str) -> str:
        return str(self._m.get(key)).format(*args)


def new_Translator(lang: str, file_path) -> ITranslator:
    with open(file_path, "rb") as f:
        last_dot_index = file_path.rfind(".")
        t = file_path[last_dot_index + 1:]
        b = f.read()
        content = yaml.load(b, Loader=yaml.FullLoader)
        m = Map.from_dict(d=content)
        return Translator(lang=lang, m=m)


class Manager():

    def __init__(self, *dirs: str):
        self.dirs: List[str] = list(dirs)

    def find(self, lang: str):
        t = self.get(lang)
        if t != None:
            return t

        if lang.find("-") > -1:
            _lang = lang.split("-")[0]
            return self.get(_lang)

        return None

    def get(self, lang: str) -> ITranslator:
        dirs = self.get_dirs()
        for dir in dirs:
            file_name = dir + ".yml"
            if files.exist(file_name):
                with open(file_name, "rb") as f:
                    last_dot_index = file_name.rfind(".")
                    t = file_name[last_dot_index + 1:]
                    b = f.read()
                    content = yaml.load(b, Loader=yaml.FullLoader)
                    m = Map.from_dict(d=content)
                    return Translator(lang=lang, m=m)
            return None
        return None

    def all(self) -> Map[str, ITranslator]:
        tm = Map[str, ITranslator]()
        dirs = self.dirs
        for dir in dirs:
            matches = files.all_file(dir, "*.yml")
            if len(matches) > 0:
                for v in matches:
                    file_name = files.file_name(v)
                    lang = file_name.strip(".yml")
                    t = new_Translator(lang=lang, file_path=v)
                    tm.set(lang, t)

        return tm

    def get_dirs(self) -> List[str]:
        if len(self.dirs) == 0:
            self.dirs = config.find_folders("i18n")
        return self.dirs


def new(*dirs: str) -> "Manager":
    return Manager(*dirs)
