import fnmatch
import os
from typing import List


def exist(file_path : str) -> bool:
    return os.path.exists(file_path)

def not_exist(file_path : str) -> bool:
    return not os.path.exists(file_path)


def is_dir(file_path : str) -> bool:
    return os.path.isdir(file_path)

def is_file(file_path : str) -> bool:
    return os.path.isfile(file_path)

def all_file(top: str, *patterns: str) -> List[str]:
    _files = []
    for root, dirs, files in os.walk(top, topdown=True):
        files.sort()
        for fname in files:
            for pt in patterns:
                if fnmatch.fnmatch(fname, pt):
                    _files.append(os.path.join(root, fname))

    return _files

def file_name(file_path : str) -> str:
    if is_file(file_path):
        return os.path.basename(file_path)
    return None



