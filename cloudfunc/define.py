# coding=utf-8

import inspect

from guniflask.annotation import Annotation, AnnotationUtils
from guniflask.context import Component


class CloudFunc(Annotation):
    def __init__(self, name=None):
        super().__init__(name=name)


def cloud_func(name: str = None):
    def wrap_func(func):
        assert inspect.isfunction(func), '@cloud_func should be applied on a function'
        AnnotationUtils.add_annotation(func, CloudFunc(name=name))
        return func

    if inspect.isfunction(name):
        f = name
        name = None
        return wrap_func(f)
    return wrap_func


class CloudClass(Component):
    pass


def cloud_class(func):
    assert inspect.isclass(func), '@cloud_class should be applied on a class'
    AnnotationUtils.add_annotation(func, CloudClass(func.__name__))
    return func
