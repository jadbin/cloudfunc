# coding=utf-8

import os
from functools import update_wrapper
import pickle
from typing import Union

import requests
from flask import current_app
from guniflask.context import BeanContext
from guniflask.service_discovery import LoadBalancedRequest

from .client import CloudFuncClient
from .errors import CloudFuncError

load_balanced_request: Union[LoadBalancedRequest, None] = None


def origin_func(name: str):
    def wrap_func(func):
        def wrapper(*args, **kwargs):
            debug = os.environ.get('CLOUDFUNC_DEBUG')
            if debug:
                client = CloudFuncClient()
                return client.run(name, *args, **kwargs)

            global load_balanced_request
            if load_balanced_request is None:
                bean_context: BeanContext = current_app.bean_context
                load_balanced_request = bean_context.get_bean_of_type(LoadBalancedRequest)
            try:
                project_name, func_name = name.split('.', maxsplit=1)
                resp = load_balanced_request.post(f'http://{project_name}/cloud-funcs/{func_name}')
                try:
                    resp.raise_for_status()
                except requests.HTTPError:
                    raise CloudFuncError(resp.text)
                return pickle.loads(resp.content)
            except Exception as e:
                raise CloudFuncError(e)

        return update_wrapper(wrapper, func)

    return wrap_func
