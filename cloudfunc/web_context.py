# coding=utf-8

from flask import Flask

from guniflask.context.default_bean_context import AnnotationConfigBeanContext
from guniflask.service_discovery import ServiceDiscoveryConfiguration
from guniflask.web.scheduling_config import WebAsyncConfiguration, WebSchedulingConfiguration
from guniflask.beans.definition import BeanDefinition

from cloudfunc.cloud_class_post_processor import CloudFuncPostProcessor


class WebContext(AnnotationConfigBeanContext):
    def __init__(self, app: Flask):
        super().__init__()
        self.app = app

    def _post_process_bean_factory(self):
        super()._post_process_bean_factory()

        bean_definition = BeanDefinition(CloudFuncPostProcessor)
        self.register_bean_definition('__cloud_func_post_processor', bean_definition)

        self._reader.register(WebAsyncConfiguration)
        self._reader.register(WebSchedulingConfiguration)
        self._reader.register(ServiceDiscoveryConfiguration)
