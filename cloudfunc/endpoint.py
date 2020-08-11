# coding=utf-8

import pickle
import traceback

from werkzeug.exceptions import HTTPException
from flask import current_app, request, abort, Response
from guniflask.web import blueprint, post_route, get_route, error_handler
from guniflask.config import settings

from cloudfunc.func_info import FuncInfo


@blueprint
class CloudFuncEndpoint:
    @post_route('/cloud-funcs/<func_name>')
    def run_func(self, func_name):
        args, kwargs = pickle.load(request.data)
        cloud_funcs = current_app.cloud_funcs
        if func_name not in cloud_funcs:
            abort(404, "No cloud function named '{}.{}'".format(settings['project_name'], func_name))
        try:
            result = cloud_funcs[func_name](*args, **kwargs)
        except Exception:
            message = traceback.format_exc()
            abort(500, message)
        else:
            return Response(response=pickle.dumps(result), content_type='application/octet-stream')

    @get_route('/cloud-funcs/<func_name>')
    def get_func_info(self, func_name):
        cloud_funcs = current_app.cloud_funcs
        if func_name not in cloud_funcs:
            abort(404, "No cloud function named '{}.{}'".format(settings['project_name'], func_name))
        info = FuncInfo(cloud_funcs[func_name])
        info.name = func_name  # rewrite name
        return info.to_dict()

    @error_handler(HTTPException)
    def handle_http_exception(self, error: HTTPException):
        return Response(response=error.description, status=error.code)
