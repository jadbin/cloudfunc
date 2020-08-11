# coding=utf-8

import inspect

from flask import current_app
from guniflask.annotation import AnnotationUtils

from guniflask.beans import BeanPostProcessorAdapter
from guniflask.context import ContextRefreshedEvent, ApplicationEvent, ApplicationEventListener

from cloudfunc.annotation import CloudClass


class CloudClassPostProcessor(BeanPostProcessorAdapter, ApplicationEventListener):
    def __init__(self):
        self.cloud_class_instances = {}

    def on_application_event(self, application_event: ApplicationEvent):
        if isinstance(application_event, ContextRefreshedEvent):
            current_app.cloud_class_instances = self.cloud_class_instances

    def post_process_after_initialization(self, bean, bean_name: str):
        bean_type = bean.__class__
        annotation = AnnotationUtils.get_annotation(bean_type, CloudClass)
        if annotation is not None:
            if inspect.isclass(bean_type):
                class_id = '{}.{}'.format(bean_type.__module__, bean_type.__name__)
                self.cloud_class_instances[class_id] = bean
        return bean
