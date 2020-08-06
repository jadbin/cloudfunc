# coding=utf-8

import inspect

from guniflask.utils.instantiation import inspect_args


class FuncInfo:
    def __init__(self, func=None, name: str = None, arg_info: list = None, type_info: dict = None, doc: str = None):
        self.name = name
        self.arg_info = arg_info or []
        self.type_info = type_info or {}
        self.doc = doc

        if func is not None:
            self.inspect_func(func)

    def inspect_func(self, func):
        assert inspect.isfunction(func), 'not a function'

        _args, _hints = inspect_args(func)

        self.arg_info = []
        for arg, default in _args.items():
            if default is inspect._empty:
                default = None
            else:
                default = repr(default)
            self.arg_info.append({'name': arg, 'default': default})

        self.type_info = {}
        for name, dtype in _hints.items():
            if inspect.isclass(dtype):
                self.type_info[name] = {'class_name': dtype.__name__, 'module_name': dtype.__module__}
            else:
                self.type_info[name] = {'repr_name': repr(dtype)}
        self.doc = func.__doc__

    def to_dict(self):
        return {
            'name': self.name,
            'arg_info': self.arg_info,
            'type_info': self.type_info,
            'doc': self.doc,
        }
