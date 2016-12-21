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
async def test():
    id = '001480598525000a60a7a150a054cafae2e09f7c5f52ba0000'
    try:
        blog = await Blog.find(id)
    except APIResourceNotFoundError as e:
        return dict(error=e.error, data=e.data, message=e.message)

    return {
        '__template__': 'test.html',
        'blog': blog
    }

@get('/bootstrap/user/{table}')
async def homepage(table):
    if check_table(table):
        return {
            '__template__': 'user-page.html',
            'table': table
        }
    else:
        return 'redirect:/bootstrap/user/blogs'

# 首页
@get('/')
async def index():
    # 当用户访问首页, 自动重定向访问/bootstrap/
    return 'redirect:/bootstrap/'


# 由于初始化了jinja2模板, 因此支持jinja2语法, 在这里{template}传入了'bootstrap'
@get('/{template}/')
async def home(template, *, tag='', page='1', size='3'):
    blogs = await Blog.findAll(orderBy='created_at desc')
    tags = [blog['summary'] for blog in blogs]
    folders = set(tags)
    if tag == '':
        num = len(tags)
    else:
        num = tags.count(tag)
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))

    if num == 0:
        blogs = []
    else:
        # 数据库获取
        # blogs = await Blog.findAll("position(? in `summary`)", [tag], orderBy='created_at desc', limit=(page.offset, page.limit))
        # 减少数据库操作, 字典构建JSON
        if tag == '':
            blogs = blogs
        else:
            blogs = [blog for blog in blogs if blog['summary'] == tag][page.offset:(page.limit+page.offset)]
    return {
        '__template__': 'blog-home.html',
        'blogs': blogs,
        'page': page,
        'tag': tag,
        'folders': folders
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
@get('/blog/{id}')
async def get_blog(id):
    try:
        blog = await Blog.find(id)
    except APIResourceNotFoundError as e:
        return dict(error=e.error, data=e.data, message=e.message)
    return {
        '__template__': 'blog-show.html',
        'blog': blog
    }
