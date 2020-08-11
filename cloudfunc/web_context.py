# coding=utf-8

from guniflask.web import WebApplicationContext
from guniflask.beans.definition import BeanDefinition

from cloudfunc.cloud_class_post_processor import CloudClassPostProcessor
from cloudfunc.endpoint import CloudFuncEndpoint


class WebContext(WebApplicationContext):

    def _post_process_bean_factory(self):
        super()._post_process_bean_factory()

        bean_definition = BeanDefinition(CloudClassPostProcessor)
        self.register_bean_definition('__cloud_class_post_processor', bean_definition)
        self._reader.register(CloudFuncEndpoint)
