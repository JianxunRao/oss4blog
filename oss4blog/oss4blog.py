#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/5 0005 上午 8:56
# @Author  : Trojx
# @File    : oss4blog.py
import ConfigParser
import os
import platform
import tempfile, shutil
import pyperclip
import oss2
import signal
import sys
import threading
import time
import urllib
from mimetypes import MimeTypes
from os.path import expanduser

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


# 使用watchdog 监控文件夹中的图像
class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpeg", "*.jpg", "*.png", "*.bmp", "*.gif", "*.tiff"]
    ignore_directories = True
    case_sensitive = False

    def process(self, event):
        if event.event_type == 'created' or event.event_type == 'modified':  # 如果是新增文件或修改的文件
            MyThread(event.src_path, 1).start()  # 开启线程

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


# 使用多线程上传
class MyThread(threading.Thread):
    def __init__(self, filePath, mode):  # filePath 文件路径 和 上传模式
        threading.Thread.__init__(self)
        self.filePath = filePath
        self.mode = mode

    def run(self):
        threadLock.acquire()
        job(self.filePath, self.mode)
        threadLock.release()


# 上传图像、复制到粘贴板、写到文件
def job(file, mode):
    if mode == 1:
        url = upload_with_full_Path(file)
    if mode == 2:
        url = upload_with_full_Path_cmd(file)
    pyperclip.copy(url)
    pyperclip.paste()
    print url
    with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
        image = '![' + url + ']' + '(' + url + ')' + '\n'
        f.write(image + '\n')


# -----------------配置--------------------
homedir = expanduser("~")  # 获取用户主目录
config = ConfigParser.RawConfigParser()
if os.path.isfile(homedir + '/oss4blog.cfg'):
    config.read(homedir + '/oss4blog.cfg')  # 读取配置文件
else:
    config.read('../oss4blog.cfg')  # 读取示例配置文件
    print 'Config file NOT exist. USE default config.'
mime = MimeTypes()
threadLock = threading.Lock()


# 优雅退出
def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    try:
        if raw_input("\nReally quit? (y/n)> ").lower().startswith('y'):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok ok, quitting")
        sys.exit(1)
    signal.signal(signal.SIGINT, exit_gracefully)


original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT, exit_gracefully)

try:
    bucket = config.get('config', 'Bucket')  # 设置  bucket
    accessKey = config.get('config', 'AccessKeyId')  # 设置  accessKey
    secretKey = config.get('config', 'AccessKeySecret')  # 设置  secretKey
    path_to_watch = config.get('config', 'PathToWatch')  # 设置   监控文件夹
    endpoint = config.get('config', 'Endpoint')  # 设置Endpoint
    enable = config.get('custom_url', 'Enable')  # 设置自定义使能 custom_url
    if enable == 'false':
        print 'custom_url not set'
    else:
        customUrl = config.get('custom_url', 'CustomUrl')
except ConfigParser.NoSectionError, err:
    print 'Error Config File:', err


# 设置编码
def setCodeingByOS():
    if 'cygwin' in platform.system().lower():
        return 'GBK'
    elif os.name == 'nt' or platform.system() == 'Windows':
        return 'GBK'
    elif os.name == 'mac' or platform.system() == 'Darwin':
        return 'utf-8'
    elif os.name == 'posix' or platform.system() == 'Linux':
        return 'utf-8'


def parseResult(result):
    print('http status: {0}'.format(result.status))
    # print('request_id: {0}'.format(result.request_id))
    # print('ETag: {0}'.format(result.etag))


# 上传文件方式 1
def upload_without_key(bucket, filePath, uploadname):
    auth = oss2.Auth(accessKey, secretKey)
    oss_bucket = oss2.Bucket(auth, endpoint, bucket)

    tmpfd, tempfilename = tempfile.mkstemp()
    shutil.copy(filePath, tempfilename)

    result = oss_bucket.put_object_from_file(uploadname, tempfilename)
    parseResult(result)
    os.close(tmpfd)


# 上传文件方式 2
def upload_with_full_Path(filePath):
    if platform.system() == 'Windows':
        fileName = "/".join("".join(filePath.rsplit(path_to_watch))[1:].split("\\"))
    else:
        fileName = "".join(filePath.rsplit(path_to_watch))[1:]
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        return 'http://' + customUrl + '/' + urllib.quote(
            fileName.decode(setCodeingByOS()).encode('utf-8'))
    else:
        return 'http://' + bucket + '.' + endpoint + '/' + urllib.quote(
            fileName.decode(setCodeingByOS()).encode('utf-8'))


# 上传文件方式 3
def upload_with_full_Path_cmd(filePath):
    if platform.system() == 'Windows':
        fileName = os.path.basename("/".join((filePath.split("\\"))))
    else:
        fileName = os.path.basename(filePath)
    upload_without_key(bucket, filePath, fileName.decode(setCodeingByOS()))
    if enable == 'true':
        return customUrl + '/' + urllib.quote(fileName.decode(setCodeingByOS()).encode('utf-8'))
    else:
        return 'http://' + bucket + '.' + endpoint + '/' + urllib.quote(
            fileName.decode(setCodeingByOS()).encode('utf-8'))


# -----------------window platform---------------start
# window下的监控文件夹变动方式-获取所有文件路径
def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.


def set_clipboard(url_list):
    for url in url_list:
        pyperclip.copy(url)
    spam = pyperclip.paste()


def window_main():
    if len(sys.argv) > 1:
        url_list = []
        for i in sys.argv[1:]:
            url_list.append(upload_with_full_Path_cmd(i))
        with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
            for url in url_list:
                image = '![' + url + ']' + '(' + url + ')' + '\n'
                print url, '\n'
                f.write(image)
        print "\nNOTE: THE MARKDOWN FORMAT URLS ALREADY SAVED IN MARKDOWN_FORMAT_URLS.txt FILE"
        set_clipboard(url_list)
        sys.exit(-1)
    print "running ... ... \nPress Ctr+C to Stop"
    before = get_filepaths(path_to_watch)
    while 1:
        time.sleep(1)
        after = get_filepaths(path_to_watch)
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added:
            url_list = []
            for i in added:
                url_list.append(upload_with_full_Path(i))
            with open('MARKDOWN_FORMAT_URLS.txt', 'a') as f:
                for url in url_list:
                    image = '![' + url + ']' + '(' + url + ')' + '\n'
                    print url, '\n'
                    f.write(image)
            print "\nNOTE: THE MARKDOWN FORMAT URLS ALREADY SAVED IN MARKDOWN_FORMAT_URLS.txt FILE"
            set_clipboard(url_list)
        if removed:
            pass
        before = after


def unix_main():
    if len(sys.argv) > 1:
        url_list = []
        for i in sys.argv[1:]:
            MyThread(i, 2).start()
        sys.exit(-1)
    print "running ... ... \nPress Ctr+C to Stop"
    observer = Observer()
    observer.schedule(MyHandler(), path=path_to_watch if path_to_watch else '.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    if os.name == 'nt' or platform.system() == 'Windows':
        window_main()  # window 下执行
    else:
        unix_main()  # mac 下执行


if __name__ == "__main__":
    main()
