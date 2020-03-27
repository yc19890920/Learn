
## pyenv
1. yum install git

2. 安装： git clone git://github.com/yyuu/pyenv.git  /usr/local/yangcheng/pyenv

3. 配置
```
echo 'export PYENV_ROOT="/usr/local/yangcheng/pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
exec $SHELL -l
```

3. 查看可以安装的Python的版本： pyenv install --list

4. 安装python：pyenv install 2.7.12 -v

5. 刷新： pyenv rehash

6. 查看已安装： pyenv versions

7. 设置全局：  pyenv global 3.5.1


```
pyenv version        # 查看当前系统使用的python版本
pyenv versions        # 查看当前系统拥有的python版本
pyenv install 3.4.1          # 安装3.4.1，可使用-v参数查看详细输出
pyenv uninstall 3.4.1         # 卸载
pyenv local 3.4.1     # local仅对当前目录及子目录生效，告诉当前目录使用版本2.7.5，
pyenv global          # 告诉全局环境使用某个版本，为了不破坏系统环境，不建议使用global设置全局版本
pyenv rehash          # 重建环境变量，每当你增删 Python 版本或带有可执行文件的包（如 pip）以后，都应该执行一次本命令
```

## 利用virtualenv 创建虚拟python环境
1. 安装 Pyenv-virtualenv插件
git clone git://github.com/yyuu/pyenv-virtualenv.git  /usr/local/yangcheng/pyenv/plugins/pyenv-virtualenv

2. 重新载入环境：  exec $SHELL
```
pyenv-virtualenv会为pyenv引入一些新的命令，例如 virtualenv/virtualenv-delete 用于创建/删除虚拟环境，
virtualenvs用于列出所有的虚拟环境，activate /deactivate用于激活和禁用虚拟环境
获取帮助： pyenv help virtualenv
```

3. 创建虚拟环境：
- 创建一个虚拟环境,py版本设置为2.7.12,名字为 django-blog：
```
创建 django-blog-env 之前，须先安装Python 2.7.12（通过系统或pyenv安装）。
django-blog 存储在~/pyenv/versions/2.7.12/envs目录中，且在~/pyenv/versions目录中建立同名符号链接。
```
>> pyenv virtualenv 2.7.12 django-blog
>> /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/bin/python
>> 
>> pyenv virtualenv 2.7.12 tornado-blog
>> /usr/local/yangcheng/pyenv/versions/2.7.12/envs/tornado-blog/bin/python

```
pyenv virtualenv 2.7.12 django-blog

New python executable in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/bin/python2.7
Also creating executable in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/bin/python

------------------------------------------
[root@localhost virtual_env_dir]# pyenv virtualenv 2.7.12 django-blog
Collecting virtualenv
  Downloading virtualenv-15.1.0-py2.py3-none-any.whl (1.8MB)
    100% |████████████████████████████████| 1.8MB 607kB/s 
Installing collected packages: virtualenv
Successfully installed virtualenv-15.1.0
You are using pip version 8.1.1, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
New python executable in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/bin/python2.7
Also creating executable in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/bin/python
Installing setuptools, pip, wheel...done.
Ignoring indexes: https://pypi.python.org/simple
Requirement already satisfied (use --upgrade to upgrade): setuptools in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/lib/python2.7/site-packages
Requirement already satisfied (use --upgrade to upgrade): pip in /usr/local/yangcheng/pyenv/versions/2.7.12/envs/django-blog/lib/python2.7/site-packages
```

4. 切换到新的虚拟环境的命令为： pyenv activate django-blog


5. 切换回系统环境： pyenv deactivate

6. 删除虚拟环境： pyenv virtualenv-delete django-blog



- [在centos上安装Python版本管理器](http://www.jianshu.com/p/1b0b50d1cd24)
- [CentOS下用pyenv 和 virtualenv 搭建单机多版本python 虚拟开发环境](http://www.cnblogs.com/MacoLee/p/5707546.html)
