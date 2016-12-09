#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from aiohttp import ClientSession, web

# 使用请求方法
from app.http_request_methods import *
# 引入orm映射类
from orm.models import *
# 使用中间件处理
from handler.api_errors import *
from handler.filters import *
from handler.handlers import *


'''view'''

# 测试
@get('/test')
async def test( *, tag='', page='1', size='10'):
    num = await Blog.countRows(where="position(? in `summary`)", args=[tag])
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll("position(? in `summary`)", [tag], orderBy='created_at desc',
                                   limit=(page.offset, page.limit))
    id = '001480598473277efc95dd2030242d481be8e830a1ef774000'
    try:
        blog = await Blog.find(id)
    except APIResourceNotFoundError as e:
        return dict(error=e.error, data=e.data, message=e.message)
    return {
        '__template__': 'test.html',
        'blogs': blogs,
        'page': page,
        'tag': tag,
        'blog': blog
    }

@get('/bootstrap/home')
async def homepage():
    return {
        '__template__': 'bootstrap-home.html'
    }

# 首页
@get('/')
async def index():
    # 当用户访问首页, 自动重定向访问/bootstrap/
    return 'redirect:/bootstrap/'

@get('/{template}/')
async def home(template, *, tag='', page='1', size='3'):
    num = await Blog.countRows(where="position(? in `summary`)", args=[tag])
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll("position(? in `summary`)", [tag], orderBy='created_at desc', limit=(page.offset, page.limit))
    # 由于初始化了jinja2模板, 因此支持jinja2语法, 在这里{template}传入了'bootstrap'
    return {
        '__template__': 'blog-home.html',
        'blogs': blogs,
        'page': page,
        'tag': tag
    }


# 注册页面
@get('/{template}/signup')
def signup(template):
    sign_type = 'signup'
    return {
        '__template__': 'blog-sign.html',
        'sign_type': sign_type
    }


# 登陆页面
@get('/{template}/signin')
def signin(template):
    sign_type = 'signin'
    return {
        '__template__': 'blog-sign.html',
        'sign_type': sign_type
    }


# 博客页面
@get('/{template}/blog/{id}')
async def get_blog(template, id):
    try:
        blog = await Blog.find(id)
    except APIResourceNotFoundError as e:
        return dict(error=e.error, data=e.data, message=e.message)
    return {
        '__template__': '%s-blog.html' % (template),
        'blog': blog
    }
