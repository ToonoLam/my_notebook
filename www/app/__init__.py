#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os
import logging
import inspect
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from handler.api_errors import APIError

app_path = os.path.join(os.path.dirname(__path__[0]), 'app')
static_path = os.path.join(app_path, 'static')
templates_path = os.path.join(app_path, 'templates')

# jinja2初始化函数
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = {
        'autoescape': kw.get('autoescape', True),
        'block_start_string': kw.get('block_start_string', '{%'),
        'block_end_string': kw.get('block_end_string', '%}'),
        'variable_start_string': kw.get('variable_start_string', '{{'),
        'variable_end_string': kw.get('variable_end_string', '}}'),
        'auto_reload': kw.get('auto_reload', True)
    }
    logging.info('set jinja2 template path: %s' % templates_path)
    env = Environment(loader=FileSystemLoader(templates_path), **options)
    filters = kw.get('filters')
    if filters is not None:
        for name, ftr in filters.items():
            env.filters[name] = ftr
    app['__templating__'] = env

# 添加一个模块的所有路由
def add_routes(app, module_name):
    try:
        mod = __import__(module_name, fromlist=['get_submodule'])
    except ImportError as e:
        raise e
    # 遍历mod的方法和属性,主要是找处理方法
    # 由于我们定义的处理方法，被@get或@post修饰过，所以方法里会有'__method__'和'__route__'属性
    for attr in dir(mod):
        # 如果是以'_'开头的，一律pass，我们定义的处理方法不是以'_'开头的
        if attr.startswith('_'):
            continue
        # 获取到非'_'开头的属性或方法
        func = getattr(mod, attr)
        # 取能调用的，说明是方法
        if callable(func):
            # 检测'__method__'和'__route__'属性
            method = getattr(func, '__method__', None)
            path = getattr(func, '__route__', None)
            # 如果都有，说明是我们定义的处理方法，加到app对象里处理route中
            if method and path:
                func = asyncio.coroutine(func)
                args = ', '.join(inspect.signature(func).parameters.keys())
                logging.info('add route %s %s => %s(%s)' % (method, path, func.__name__, args))
                # app.router.add_route(method, path, func)
                app.router.add_route(method, path, RequestHandler(func))


# 添加静态文件夹的路径
def add_static(app):
    # 取当前__init__文件所在的绝对路径,通过os模块拼接static文件的绝对路径
    app.router.add_static('/static/', static_path)
    logging.info('add static %s => %s' % ('/static/', static_path))


# RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，
# URL函数不一定是一个coroutine，因此我们用RequestHandler()来封装一个URL处理函数。
# 调用URL函数，然后把结果转换为web.Response对象，这样，就完全符合aiohttp框架的要求：

class RequestHandler(object): # 初始化一个请求处理类

    def __init__(self, func):
        self._func = func

    async def __call__(self, request):#任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用
        # 获取函数的参数表
        required_args = inspect.signature(self._func).parameters
        logging.info('required args: %s' % required_args)

        # 获取从GET或POST传进来的参数值，如果函数参数表有这参数名就加入
        kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}

        # 获取match_info的参数值，例如@get('/blog/{id}')之类的参数值
        kw.update(dict(**request.match_info))

        # 如果有request参数的话也加入
        if 'request' in required_args:
            kw['request'] = request

        # 检查参数表中有没参数缺失
        for key, arg in required_args.items():
            # request参数不能为可变长参数
            if key == 'request' and arg.kind in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                return web.HTTPBadRequest(text='request parameter cannot be the var argument.')
            # 如果参数类型不是变长列表和变长字典，变长参数是可缺省的
            if arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                # 如果还是没有默认值，而且还没有传值的话就报错
                if arg.default == arg.empty and arg.name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)

        logging.info('call with args: %s' % kw)
        try:
            return await self._func(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)
