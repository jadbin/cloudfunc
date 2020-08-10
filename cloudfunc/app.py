# coding=utf-8

from typing import List

from flask import Flask
from guniflask.annotation import AnnotationUtils
from guniflask.config import AppConfig
from guniflask.utils.traversal import walk_modules

from cloudfunc.annotation import CloudFunc, CloudClass
from cloudfunc.web_context import WebContext


def create_app(name, settings=None, includes: List[str] = None):
    app = Flask(name)
    config = AppConfig(app, app_settings=settings)
    bean_context = create_bean_context(app)
    app.bean_context = bean_context
    config.init_app()
    with app.app_context():
        if includes:
            bean_context.scan(*includes)
        refresh_bean_context(bean_context)
    if includes:
        register_cloud_funcs(app, includes)
    return app


def create_bean_context(app) -> WebContext:
    bean_context = WebContext(app)
    return bean_context


def refresh_bean_context(bean_context: WebContext):
    bean_context.refresh()


def register_cloud_funcs(app, includes: List[str]):
    cloud_funcs = {}
    cloud_class_instances: dict = app.cloud_class_instances
    registered_funcs = set()

    def iter_cloud_funcs():
        for m in includes:
            for module in walk_modules(m):
                for obj in vars(module).values():
                    annotation = AnnotationUtils.get_annotation(obj, CloudFunc)
                    if annotation is not None and obj not in registered_funcs:
                        name = annotation['name']
                        if name is None:
                            name = obj.__name__
                        yield name, obj
                        registered_funcs.add(obj)
                    annotation = AnnotationUtils.get_annotation(obj, CloudClass)
                    if annotation is not None and obj.__module__ == module.__name__:
                        for subobj in vars(obj).values():
                            subannotation = AnnotationUtils.get_annotation(subobj, CloudFunc)
                            if subannotation is not None:
                                name = subannotation['name']
                                if name is None:
                                    name = subobj.__name__
                                class_id = '{}.{}'.format(obj.__module__, obj.__name__)
                                method = getattr(cloud_class_instances[class_id], subobj.__name__)
                                yield name, method

    for name, func in iter_cloud_funcs():
        cloud_funcs[name] = func
    app.cloud_funcs = cloud_funcs
