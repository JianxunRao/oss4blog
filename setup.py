#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/5 0005 上午 11:00
# @Author  : Trojx
# @File    : setup.py
from distutils.core import setup

setup(
    name='oss4blog',
    version='0.0.3',
    author='Trojx',
    author_email='raojianxun@126.com',
    packages=['oss4blog'],
    scripts=['oss4blog/oss4blog.py'],
    url='http://pypi.python.org/pypi/oss4blog/',
    license='The MIT License',
    description='Useful util to use Aliyun OSS to build image hosting for static blog.',
    long_description='Useful util to use Aliyun OSS to build image hosting for static blog.',
    install_requires=[
        'pyperclip', 'oss2', 'watchdog',],
    entry_points={
        'console_scripts':[
            'oss4blog = oss4blog.oss4blog:main'
        ]
    },
)