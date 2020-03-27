 apt-get install libc6-dev gcc
 apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm

1. 安装pyenv
git clone https://github.com/yyuu/pyenv.git  /home/python/pyenv

2. 配置
```
echo 'export PATH=/home/python/pyenv/bin:$PATH' >> ~/.bashrc
echo 'export PYENV_ROOT=/home/python/pyenv' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source .bashrc 
```

3. 查看可以安装的Python的版本： pyenv install --list

4. 安装python：pyenv install 2.7.12 -v

5. 刷新： pyenv rehash

6. 查看已安装： pyenv versions

7. 设置全局：  pyenv global 3.5.1

```
pyenv version        # 查看当前系统使用的python版本
pyenv versions        # 查看当前系统拥有的python版本
pyenv install 3.4.1          # 安x装3.4.1，可使用-v参数查看详细输出
pyenv uninstall 3.4.1         # 卸载
pyenv local 3.4.1     # local仅对当前目录及子目录生效，告诉当前目录使用版本2.7.5，
pyenv global          # 告诉全局环境使用某个版本，为了不破坏系统环境，不建议使用global设置全局版本
pyenv rehash          # 重建环境变量，每当你增删 Python 版本或带有可执行文件的包（如 pip）以后，都应该执行一次本命令
```

## 安装pyenv-virtualenv
1. 安装 Pyenv-virtualenv插件
```
git clone https://github.com/yyuu/pyenv-virtualenv.git   /home/python/pyenv/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
source .bashrc
```

```
pyenv-virtualenv会为pyenv引入一些新的命令，例如 virtualenv/virtualenv-delete 用于创建/删除虚拟环境，
virtualenvs用于列出所有的虚拟环境，activate /deactivate用于激活和禁用虚拟环境
获取帮助： pyenv help virtualenv
```

2. 创建虚拟环境：
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

3. 切换到新的虚拟环境的命令为： pyenv activate django-blog


4. 切换回系统环境： pyenv deactivate

5. 删除虚拟环境： pyenv virtualenv-delete django-blog


- [pyenv简介——Debian/Ubuntu中管理多版本Python](http://www.malike.net.cn/blog/2016/05/21/pyenv-tutorial/)
