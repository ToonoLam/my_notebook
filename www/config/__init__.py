#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 数据库默认设置
db_config = {
    'user': 'toono',
    'password': 'passwd',
    'db': 'orm_data'
}

# jinja2默认设置
jinja2_config = dict()

# cookie默认设置
COOKIE_NAME = 'MyBlogSession'
COOKIE_KEY = 'MyBlog'

__all__ = ['db_config', 'jinja2_config', 'COOKIE_NAME', 'COOKIE_KEY']

