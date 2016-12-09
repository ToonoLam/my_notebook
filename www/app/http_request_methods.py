#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools


# 定义各种url处理函数, http请求的8种动作
# 函数经次函数装饰后即带上了__method__、__route__属性

# method 1
def get(path):
    '''
    装饰函数
    Define decorator @get('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 2
def post(path):
    '''
    装饰函数
    Define decorator @post('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 3
def put(path):
    '''
    装饰函数
    Define decorator @put('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'PUT'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 4
def head(path):
    '''
    装饰函数
    Define decorator @head('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'HEAD'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 5
def delete(path):
    '''
    装饰函数
    Define decorator @delete('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'DELETE'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 6
def trace(path):
    '''
    装饰函数
    Define decorator @trace('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'TRACE'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 7
def options(path):
    '''
    装饰函数
    Define decorator @options('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'OPTIONS'
        wrapper.__route__ = path
        return wrapper

    return decorator

# method 8
def connect(path):
    '''
    装饰函数
    Define decorator @connect('/path')
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        wrapper.__method__ = 'CONNECT'
        wrapper.__route__ = path
        return wrapper

    return decorator
