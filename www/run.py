#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio
import logging
from aiohttp import web

# 初始化web app
from app import init_jinja2, add_routes, add_static
# 获取中间件处理需要的工厂函数和jinja模板过滤器
from handler.factorys import *
from handler.filters import *
# 从连接池获取连接并初始化数据库
from orm import create_pool

logging.basicConfig(level=logging.INFO)

async def create_server(loop, config_mod_name):
    try:
        # __import__('config', fromlist=['get config']) == from app.config import __init__
        config = __import__(config_mod_name, fromlist=['get config'])
    except ImportError as e:
        raise e

    # 从连接池中获得连接, 使用config.db_config设置数据库参数
    await create_pool(loop, **config.db_config)
    # 创建一个web服务器实例,使用默认loop,request接收前通过多个中间件工厂函数处理清洗
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, data_factory, response_factory])
    add_routes(app, 'app.manages')
    add_routes(app, 'app.apis')
    add_routes(app, 'app.views')
    add_static(app)
    # 初始化jinjia2模板,使用日期过滤器和markdown转换过滤器,其余初始化设置可以在config中传入
    init_jinja2(app, filters=dict(datetime=datetime_filter, marked=marked_filter), **config.jinja2_config)
    # 创建服务器实例
    server = await loop.create_server(app.make_handler(), '127.0.0.1', 9999)
    logging.info('server started at http://127.0.0.1:9999...')
    return server

if __name__ == '__main__':
    # 创建一个异步事件回路实例
    loop = asyncio.get_event_loop()
    # 创建一个服务器实例放入到异步事件回路
    loop.run_until_complete(create_server(loop, 'config'))
    # 异步事件回路永久运行
    loop.run_forever()