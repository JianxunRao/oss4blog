#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/5 0005 上午 11:00
# @Author  : Trojx
# @File    : setup.py
from distutils.core import setup

setup(
    name='oss4blog',
    version='0.0.1',
    author='Trojx',
    author_email='raojianxun@126.com',
    packages=['oss4blog'],
    scripts=['oss4blog/oss4blog.py'],
    url='http://pypi.python.org/pypi/oss4blog/',
    license='LICENSE',
    description='Useful util to use Aliyun OSS to build image hosting for static blog.',
    long_description=open('README.md').read(),
    install_requires=[
        'pyperclip', 'oss2', 'watchdog',],
)