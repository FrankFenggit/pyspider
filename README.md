[TOC]



# pyspider

求职者爬虫

## 框架简介

Python中强大的Spider(WebCrawler)系统。**[现在试试！](http://demo.pyspider.org/)**

- 用Python编写脚本
- 功能强大的WebUI，包括脚本编辑器、任务监视器、项目经理和结果查看器
- [MySQL](https://www.mysql.com/), [MongoDB](https://www.mongodb.org/), [Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), [Elasticsearch](https://www.elastic.co/products/elasticsearch); [PostgreSQL](http://www.postgresql.org/) with [SQLAlchemy](http://www.sqlalchemy.org/) as database 作为数据库后端
- [RabbitMQ](http://www.rabbitmq.com/), [Beanstalk](http://kr.github.com/beanstalkd/), [Redis](http://redis.io/) and [Kombu](http://kombu.readthedocs.org/) 作为消息队列
- 任务优先，重试，定期，按年龄等.
- 分布式架构，爬行Javascript页面，Python 2和3，等等.

教程：http://docs.pyspider.org/en/latest/tutorial/
文件：http://docs.pyspider.org/
发布说明：https://github.com/binux/pyspider/releases

## 环境准备

1. PC机器 （win7旗舰版 64）

2. python3.7.3 （建议pip升下级 python -m pip install --upgrade pip）

3. phantomjs

   - [ ] 下载

     | 官方下载     | https://phantomjs.org/download.html                  |            |
     | ------------ | ---------------------------------------------------- | ---------- |
     | 中文         | http://wenku.kuryun.com/docs/phantomjs/download.html |            |
     | 淘宝镜像下载 | http://npm.taobao.org/dist/phantomjs/                | 推荐用这个 |

   - [ ] 进入解压文件夹中，左键双击可执行文件 `phantomjs.exe` 进入傻瓜式安装步骤

   - [ ] 配置环境变量 （命令行测试 phantomjs  ok）

4. pyspider

   - [ ] pip install pyspider
   - [ ] 命令行运行  pyspider （这里可能会报错，见FQ列表）
   - [ ] 浏览器运行脚本编辑界面`WebUI` `http://localhost:5000/`
   - [ ] 点击“create”，写python脚本就好了

## FQ（踩过的坑）

### python3.7不兼容pyspider问题(出现占用关键字的问题)

Python 3.5中引入了async，它们在Python 3.7中成为关键字，所以需要替换一下关键字。

（约有10来处吧 ：async --> async_mod）

### Exception: HTTP 599: SSL certificate problem: unable to get local issuer certificate

原因：这个错误是因为你要爬取的网站带有HTTPS的验证，而你本地找不到这个验证所以产生了这个错误，错误有两种解决方法：原因：这个错误是因为你要爬取的网站带有HTTPS的验证，而你本地找不到这个验证所以产生了这个错误，错误有两种解决方法：（个人推荐方法1，git下来最新的不是稳定版）

第一种：在你需要爬取的网址后面的在

> crawl 方法中加入忽略证书验证的参数，validate_cert=False，
>  即self.crawl(url, callback=method_name, validate_cert=False)



第二种：使用git下来的最新的[pyspider源码](http://github.com/binux/pyspider )

把\site-packages目录下的pyspider整个文件夹删掉，用git下的源码里的pyspider整体复制过去，重启pyspider all，再次浏览器中RUN

### 在实际的调试中发现pyspider的**Web预览界面只有一点非常小**（非必须）

 原因：web预览框过小的原因在于页面元素的css属性height被替换为60px
 所以我们需要更改CSS文件的内容，但是这个应该不是所有浏览器都通用，只是测试了**Chrome浏览器**是可以的
 在你的pyspider目录下

> C:\Python\Python37\Lib\site-packages\pyspider\webui\static

我的是这个，找到这样的一个文件叫debug.min.css有的也是debug.min


备份一个人，替换错了会把**爬虫项目的整个运行界面都给整没！！！**亲测  真的没了！真的好用！
[debug.min.css替换地址](https://github.com/ok2fly/pyspider/blob/abcfc98970be27dd97901479675ce6df39be63fc/pyspider/webui/static/debug.min.css)
 把里面的东西复制过去就行，需要在web显示界面下再次点击run按钮，即可显示正常大小









## 参考资料

[官方文档]: http://docs.pyspider.org/en/latest/
[开源地址]: http://github.com/binux/pyspider
[中文文档]: http://www.pyspider.cn/
[入门视频]: https://www.bilibili.com/video/BV1vW411T7qD?from=search&amp;seid=8495872054225096531

# web开发： jobsWeb

- 拿到爬虫数据，解析，展示
- 引用flask框架
- 开发工具：pycharm

## 雕虫小计

### model逆向（model代码自动生成，一个字爽）

使用 flask-sqlacodegen工具

```powershell
pip install flask-sqlacodegen

flask-sqlacodegen sqlite:///D:/codes/spider/jobsWeb/data/result.db --outfile 'model.py' --flask
```