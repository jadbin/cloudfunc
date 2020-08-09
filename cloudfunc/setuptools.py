# coding=utf-8

from typing import List, Union
from os.path import isfile

after_setup = {}


def setup(name: str = None,
          version: str = None,
          description: str = None,
          long_description: str = None,
          author: str = None,
          author_email: str = None,
          includes: Union[str, List[str]] = None,
          install_requires: Union[str, List[str]] = None,
          cloudfunc_requires: Union[str, List[str]] = None):
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

    if cloudfunc_requires is None:
        # load cloudfunc_requirements.txt
        cloudfunc_requires = _read_requires('cloudfunc_requirements.txt')
    elif isinstance(cloudfunc_requires, str):
        cloudfunc_requires = [cloudfunc_requires]
    after_setup['cloudfunc_requires'] = cloudfunc_requires


def _read_requires(file: str) -> List[str]:
    requires = []
    if isfile(file):
        with open('requirements.txt', 'r') as f:
            for line in f:
                s = line.strip()
                if s:
                    requires.append(s)
    return requires
