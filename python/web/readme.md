
- [python 各种 web 框架对比](https://hacpai.com/article/1549524942933)
- [Fast and elegant Vibora was designed from scratch to be efficient.](https://vibora.io/)
- [docs vibora](https://docs.vibora.io/)
- [docs vibora](https://docs.vibora.io/))

##### 可以考虑学习一下 Vibora / Falcon / Tornado / Flask

## 0 引言
   python在web开发方面有着广泛的应用。鉴于各种各样的框架，对于开发者来说如何选择将成为一个问题。为此，我特此对比较常见的几种框架从性能、使用感受以及应用情况进行一个粗略的分析。
## 1 Django
   Django是一个开放源代码的Web应用框架，由Python写成。
   采用了MTV的框架模式，即模型M，模板T和视图V。
   它最初是被开发来用于管理劳伦斯出版集团旗下的一些以新闻内容为主的网站的，即是CMS（内容管理系统）软件。
   Django与其他框架比较，它有个比较独特的特性，支持orm，将数据库的操作封装成为python，对于需要适用多种数据库的应用来说是个比较好的特性。
   不过这种特性，已经有其他库完成了，sqlalchemy.

## 2 Flask
   Flask是一个使用 Python 编写的轻量级 Web 应用框架。其 WSGI 工具箱采用 Werkzeug ，模板引擎则使用 Jinja2 。Flask使用 BSD 授权。
   Flask也被称为 “microframework” ，因为它使用简单的核心，用 extension 增加其他功能。Flask没有默认使用的数据库、窗体验证工具。
   Flask 很轻，花很少的成本就能够开发一个简单的网站。非常适合初学者学习。
   Flask 框架学会以后，可以考虑学习插件的使用。例如使用 WTForm + Flask-WTForm 来验证表单数据，用 SQLAlchemy + Flask-SQLAlchemy 来对你的数据库进行控制。

## 3 Tornado
   Tornado是一种 Web 服务器软件的开源版本。Tornado 和现在的主流 Web 服务器框架（包括大多数 Python 的框架）有着明显的区别：它是非阻塞式服务器，而且速度相当快。
   得利于其 非阻塞的方式和对epoll的运用，Tornado 每秒可以处理数以千计的连接，因此 Tornado 是实时 Web 服务的一个 理想框架。
   不过现在与众多的框架比较，Tornado已经被抛在了后面，Django已经超过了它，更不说其他框架了，只能说Tornado使用纯python开发的性能还是不能与其他框架借助于cython开发的性能相比。

## 4 web.py
   web.py 是一个Python 的web 框架，它简单而且功能强大。
   web.py 是公开的，无论用于什么用途都是没有限制的。
   而且相当的小巧，应当归属于轻量级的web 框架。
   但这并不影响web.py 的强大，而且使用起来很简单、很直接。
   在实际应用上，web.py 更多的是学术上的价值，因为你可以看到更多web 应用的底层，这在当今“抽象得很好”的web 框架上是学不到的 ：）

## 5 Aiohttp
   高性能异步web框架，既有客户端的也有服务端的，还支持web-socket
   
## 6 Sanic
   与flask类似，并支持异步
   
## 7 Vibora
   旨在成为最快的python web框架。
   vibora的高性能依赖于 cython实现的uvloop异步框架及cython实现的http_parser, 再加上一些cython构建的web组件，比如 模板，user-route等。目前还处于测试阶段。

## 8 Bottle
   Bottle是一个简单高效的遵循WSGI的微型python Web框架。
   说微型，是因为它只有一个文件，除Python标准库外，它不依赖于任何第三方模块。
   
## 9 Falcon
   Falcon是一个构建云API的高性能Python框架，它鼓励使用REST架构风格，尽可能以最少的力气做最多的事情。
   
## 10 weppy
   性能优于flask的一个全栈web框架

11 并发请求对比
Tornado	14197	5.0.2
Django	22823	2.0.6
Flask	37487	1.0.2
Aiohttp	61252	3.3.2
Sanic	119764	0.7.0
Vibora	368456	0.0.6