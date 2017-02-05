[![](https://img.shields.io/badge/python-2.7.11-blue.svg)](https://pypi.python.org/pypi/oss4blog)
### 使用阿里云OSS搭建静态博客图床

### 工作流程

> python 监控文件夹 --> 文件新增 --> 使用 oss sdk 上传到 阿里云oss  --> 生成外链到粘贴板 --> 复制图片外链到博客

### 安装
> pip install oss4blog

### 配置

登录[阿里云OSS](https://oss.console.aliyun.com/index#/)
新建一个**Bucket**

![http://cdn.trojx.me/blog_pic/new_bucket.png](http://cdn.trojx.me/blog_pic/new_bucket.png)

获取此Bucket的Endpoint

![http://cdn.trojx.me/blog_pic/get_endpoint.png](http://cdn.trojx.me/blog_pic/get_endpoint.png)

并在[Access Key管理](https://ak-console.aliyun.com)中获取`accessKey` ,`secretKey`相关信息: 

![http://cdn.trojx.me/blog_pic/get_AK_SK.png](http://cdn.trojx.me/blog_pic/get_AK_SK.png)

在home目录下新建配置文件`oss4blog.cfg` 例如`C:\Users\Administrator\oss4blog.cfg`
`Bucket`为Bucket名称
`AccessKeyId` 为阿里云账户的AccessKeyId
`AccessKeySecret`为阿里云账户的AccessKeySecret
`PathToWatch` 为截图自动保存的目录
`Endpoint` 为当前Bucket的外网Endpoint
`oss4blog.cfg`内容如下
`Enable` 是否使用自定义域名
`CustomUrl` 自定义域名(开头不含`http://`)

```
[config]
Bucket = trojx-me
AccessKeyId = *****
AccessKeySecret = *****
PathToWatch = C:\Users\Administrator\PycharmProjects\oss4blog\path_to_watch
Endpoint = oss-cn-hangzhou.aliyuncs.com

[custom_url]
Enable = false
CustomUrl = cdn.trojx.me

```
### 运行
#### 监听模式
打开终端或cmd
> oss4blog  

将会监听PathToWatch内的文件变动，上传图片

### 关于
[本项目](https://github.com/JianxunRao/oss4blog)源自开源项目[qiniu4blog](https://github.com/wzyuliyang/qiniu4blog),是后者面向阿里云OSS的实现
