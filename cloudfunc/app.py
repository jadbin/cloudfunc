# coding=utf-8

from flask import Flask
from guniflask.annotation import AnnotationUtils
from guniflask.config.app_config import AppConfig
from guniflask.utils.traversal import walk_modules

from cloudfunc.annotation import CloudFunc, CloudClass
from cloudfunc.web_context import WebContext


def create_app(name, settings=None):
    app = Flask(name)
    config = AppConfig(app, app_settings=settings)
    bean_context = create_bean_context(app)
    app.bean_context = bean_context
    config.init_app()
    with app.app_context():
        refresh_bean_context(bean_context)
    register_cloud_funcs(app)


def create_bean_context(app) -> WebContext:
    bean_context = WebContext(app)
    bean_context.scan(app.name)
    return bean_context


def refresh_bean_context(bean_context: WebContext):
    bean_context.refresh()


def register_cloud_funcs(app):
    cloud_funcs = {}
    cloud_class_instances: dict = app.cloud_class_instances
    registered_funcs = set()

    def iter_cloud_funcs():
        for module in walk_modules(app.name):
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
                        subannotation = AnnotationUtils.get_annotation(obj, CloudFunc)
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
