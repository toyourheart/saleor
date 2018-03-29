[![Saleor](http://getsaleor.com/mr-saleor-readme.png)](http://getsaleor.com)


Saleor
======

* * *

Usage
-----

See the [Saleor docs](https://saleor.readthedocs.io) for installation and deployment instructions.

[mac使用](https://saleor.readthedocs.io/en/latest/gettingstarted/installation-macos.html)
-----
准备： $ `brew install python3 git nodejs PostgreSQL`

gtk+
用来创建pdf的
$ `brew install cairo pango gdk-pixbuf libffi`

安装
-----
1. 克隆项目
$ `git clone https://github.com/mirumee/saleor.git`
2. 进入目录
$ `cd saleor/`

3. 如下
 + 创建 python3 虚拟机
$ `python3 -m venv name_env`
 + 激活虚拟机
$ `source name_env/bin.active`
 + 如果你的系统安装了多个Python版本，需要指定virtualenv使用的版本。例如，命令
$ `virtualenv ll_env --python=python3`
 + 在 python3 虚拟机里 安装信赖包
$ `pip3 install -r requirements.txt`

4.创建密钥，要保密
$ `export SECRET_KEY='mysecretkey'`

5.创建数据库及超级用户
 + 安装数据库
 $ `brew install PostgreSQL`
 安装后，有提示启动命令
 + [使用数据库的方法] (https://www.jianshu.com/p/da3e9e92f978) 
 前台启动
 $ `postgres -D /usr/local/var/postgres`
 或者后台启动，选其中一样
 $ `brew services start postgresql`
 + 创建数据库
 $ `createdb saleor`
 + 进入数据库
 $ `psql postgres`
 + 创建超级用户 [参考官网](https://www.postgresql.org/docs/current/static/sql-createrole.html)
   下面的 saleor 是此项目默认的用户名，语句的后面刻加 ; 号
 postgres=# `CREATE ROLE saleor WITH CREATEDB CREATEROLE SUPERUSER LOGIN PASSWORD 'jw8s0F4';`
 查看是否创建成功
 postgres=# `\du`

6. 迁移数据库
$ `python manage.py migrate`

7. 安装前端依赖项
$ `npm install`

8. 准备前端资产:
$ `npm run build-assets`

9. 编译电子邮件:
$ `npm run build-emails`

10. 启动服务器
$ `python manage.py runserver`

11. 用浏览器打开 (http://127.0.0.1:8000)
Demo
----

Want to see Saleor in action?

[Saleor live demo](http://demo.getsaleor.com/)

[Saleor Dashboard (admin area) demo](http://demo.getsaleor.com/dashboard/)

Or launch the demo on a free Heroku instance.

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Login credentials: `admin@example.com`/`admin`



### Mirumee Software

http://mirumee.com
