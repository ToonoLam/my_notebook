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

'''manages'''

# 管理页面
@get('/{template}/manage')
def manage(template):
    return 'redirect:/%s/manage/users' % (template)


# 管理用户、博客、评论
@get('/{template}/manage/{table}')
def manage_table(template, table):
    if check_table(table):
        return {
            '__template__': '%s-manage.html' % (template),
            'table': table
        }
    else:
        return 'redirect:/%s/manage/users' % (template)


# 创建博客
@get('/{template}/manage/blogs/create')
def manage_create_blog(template):
    return {
        '__template__': '%s-blog_edit.html' % (template)
    }


# 修改博客
@get('/{template}/manage/blogs/edit')
def manage_edit_blog(template):
    return {
        '__template__': '%s-blog_edit.html' % (template)
    }
