# coding=utf-8

from os.path import isfile
from typing import List, Union

after_setup = {}


def setup(name: str = None,
          version: str = None,
          description: str = None,
          long_description: str = None,
          author: str = None,
          author_email: str = None,
          includes: Union[str, List[str]] = None,
          install_requires: Union[str, List[str]] = None,
          pypi_url: str = None):
    after_setup.clear()

    if name is None:
        raise ValueError("'name' cannot be None")
    after_setup['name'] = name
    if version is None:
        raise ValueError("'version' cannot be None")
    after_setup['version'] = version
    after_setup['description'] = description
    after_setup['long_description'] = long_description
    after_setup['author'] = author
    after_setup['author_email'] = author_email

    if includes is None:
        includes = [name]
    elif isinstance(includes, str):
        includes = [includes]
    after_setup['includes'] = includes

    if install_requires is None:
        # load requirements.txt
        install_requires = _read_requires('requirements.txt')
    elif isinstance(install_requires, str):
        install_requires = [install_requires]
    after_setup['install_requires'] = install_requires

    after_setup['pypi_url'] = pypi_url


def _read_requires(file: str) -> List[str]:
    requires = []
    if isfile(file):
        with open('requirements.txt', 'r') as f:
            for line in f:
                s = line.strip()
                if s:
                    requires.append(s)
    return requires


def run_setup(fname) -> dict:
    if fname is None or not isfile(fname):
        raise FileNotFoundError(fname)
    code = compile(open(fname, 'rb').read(), fname, 'exec')
    cfg = {
        "__builtins__": __builtins__,
        "__name__": "__config__",
        "__file__": fname,
        "__doc__": None,
        "__package__": None
    }
    exec(code, cfg, cfg)
    return cfg
