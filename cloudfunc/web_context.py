# coding=utf-8

from guniflask.web import WebApplicationContext
from guniflask.beans.definition import BeanDefinition

from cloudfunc.cloud_class_post_processor import CloudFuncPostProcessor
from cloudfunc.cloud_func_endpoint import CloudFuncEndpoint


class WebContext(WebApplicationContext):

    def _post_process_bean_factory(self):
        super()._post_process_bean_factory()

        bean_definition = BeanDefinition(CloudFuncPostProcessor)
        self.register_bean_definition('__cloud_func_post_processor', bean_definition)
        self._reader.register(CloudFuncEndpoint)
