import os
import sys
from typing import List

from bee.ext import files as files
from bee.config.source import EnvSource, Source, cover_option, FileSource, ByteDataSource
from bee.data.map import Map


exts: List[str] = [".yml", ".yaml", ".json"]


class Unmarshaler():
    """
    Unmarshaler is custom unmarshal interface for Config.Unmarshal method.
    """

    def Unmarshal(self):
        pass


class Manager():

    def __init__(self):
        self.loaded: bool = False
        self.autoLoad: bool = False

        self.env: EnvSource = EnvSource()

        self.options: Map = None
        self.profiles: List[str] = []
        self.dirs: List[str] = []
        self.name: str = None
        self.srcs: List[Source] = []

        self.defaults: Map = Map()

    def set_name(self, name: str):
        self.name = name

    @staticmethod
    def new(name: str) -> "Manager":
        m = Manager()
        if not name:
            m.set_name(name)
        else:
            m.set_name("app")

        m.set_default_value("banner", True)
        m.set_env_prefix("BEE")
        return m

    def set_default_value(self, name: str, value):
        # if not self.loaded:
        #     self.load(True)
        cover_option(self.defaults, name.lower(), value)

    def set_env_prefix(self, prefix: str):
        self.env.set_prefix(prefix)

    def add_folder(self, *dirs: str):
        length = len(dirs)
        if length > 0:
            for v in dirs:
                self.dirs.append(v)

    def find_file(self, name: str, *exts) -> str:
        """
        find_file searches all config directories and return the first found file.
        :param name:
        :param exts:
        :return:
        """
        for dir in self.dirs:
            for ext in exts:
                path = dir + "/" + name + ext
                if files.exist(path):
                    return path
                else:
                    return ""

    def find_files(self, name: str, *exts) -> List[str]:
        """
        find_files searches all config directories and return all found files.
        :param name:
        :param exts:
        :return:
        """
        fs = []
        for dir in self.dirs:
            for ext in exts:
                path = dir + "/" + name + ext
                if files.exist(path):
                    fs.append(path)
        return fs

    def find_folder(self, name) -> str:
        """
        find_folder earches all config directories and return the first found folder.
        :param name:
        :return:
        """
        for dir in self.dirs:
            path = dir + "/" + name
            if files.exist(path):
                return path
            else:
                return ""

    def find_folders(self, name) -> List[str]:
        dirs = []
        for dir in self.dirs:
            path = dir + "/" + name
            if files.exist(path):
                dirs.append(path)
        return dirs

    def load(self, force: bool):
        if self.loaded and not force:
            return None
        self.options = Map()
        """read env source"""
        self.load_source(self.env)

        """read file source"""
        srcs = self.find_file_sources()
        self.load_source(*srcs)

        """read self.srcs"""
        self.load_source(*self.srcs)

        self.loaded = True

    def load_source(self, *srcs: Source):
        for src in srcs:
            opts = src.load()
            self.options.merge(opts)

    def get(self, key: str):
        if not self.loaded:
            self.load(True)
        opt = self.options.find(key)
        default = self.defaults.find(key)
        if default == None:
            return opt
        elif opt == None:
            return default
        return opt

    def find_file_sources(self) -> List[Source]:
        srcs = []
        # step 1: if len(self.dirs)==0, read default folders
        if len(self.srcs) == 0:
            # TODO: to be continued...
            self.add_folder(os.path.join(sys.path[1], "config"))
            self.add_folder(".")

        # step 2: else read self.dirs
        for dir in self.dirs:
            for ext in exts:
                for profile in self.profiles:
                    path = dir + "/" + self.name + "." + profile + ext
                    if files.exist(path):
                        srcs.append(FileSource(path))

        for dir in self.dirs:
            for ext in exts:
                path = dir + "/" + self.name + ext
                if files.exist(path):
                    srcs.append(FileSource(path))
        return srcs

    def set_profiles(self, *profiles: str):
        for profile in profiles:
            self.profiles.append(profile)

    def add_source(self, *srcs: Source):
        for src in srcs:
            self.srcs.append(src)

    def add_byte_source(self, d: bytes, t: str):
        ds = ByteDataSource(d, t)
        self.add_source(ds)

    def bind_env(self, key: str, env_key: str):
        self.env.set_aliases(key, env_key)


