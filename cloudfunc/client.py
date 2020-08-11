# coding=utf-8

import os
import pickle

import requests

from .errors import CloudFuncError


class CloudFuncClient:
    def __init__(self, serve_address: str = None):
        if serve_address is None:
            serve_address = os.environ['CLOUDFUNC_SERVE_ADDRESS']
        assert serve_address is not None, 'cloudfunc-serve address is not given'
        self.serve_address = serve_address
        self.session = requests.Session()

    def run(self, cloud_func_name: str, *args, **kwargs):
        data = pickle.dumps((args, kwargs))
        try:
            print('>>>>>', f'http://{self.serve_address}/cloud-funcs/run')
            resp = self.session.post(
                f'http://{self.serve_address}/cloud-funcs/run',
                params={'name': cloud_func_name},
                data=data
            )
        except Exception as e:
            raise CloudFuncError(e)
        else:
            try:
                resp.raise_for_status()
            except requests.HTTPError:
                raise CloudFuncError(resp.content)
            return pickle.loads(resp.content)
