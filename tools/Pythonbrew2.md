
## 一、安装Pythonbrew
> 通过pythonbrew工具实现多版本python管理，首先安装pythonbrew。
> 安装前确保系统有以下包
>> `sudo apt-get install curl build-essential libbz2-dev libsqlite3-dev zlib1g-dev libxml2-dev libxslt1-dev libreadline5 libgdbm-dev libgdb-dev libxml2 libssl-dev tk-dev libgdbm-dev libexpat1-dev libncursesw5-dev`


#### 安装 Python 发布版本，dev包必须安装，很多用pip安装包都需要编译
> `sudo apt-get install python2.7 python2.7-dev python3.2 python3.2-dev`

#### 很多pip安装的包都需要libssl和libevent编译环境
> `sudo apt-get install build-essential libssl-dev libevent-dev libjpeg-dev libxml2-dev libxslt-dev`

#### 开始安装pythonbrew

```
使用官网推荐的方法安装：
curl -kL http://xrl.us/pythonbrewinstall | bash
以上命令把Pythonbrew自动安装在~/.pythonbrew目录下。

1、使用easy_install工具安装，用命令：which easy_install查看是否安装该工具；没有输出则没安装，需要先安装easy_install
$ sudo easy_install pythonbrew
2、或者使用官网推荐的方法安装：
curl -kL http://xrl.us/pythonbrewinstall | bash
以上命令把Pythonbrew自动安装在~/.pythonbrew目录下；
```

## 二、Pythonbrew配置

```
运行：
$ pythonbrew_install
会提示把下面内容添加到~/.bashrc文件中（Please add the following line to the end of your ~/.bashrc）,不用运行上面的命令手动把下面内容添加到文件中就可以了；
[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source "$HOME/.pythonbrew/etc/bashrc"
[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source "$HOME/.pythonbrew/etc/bashrc"
[[ -s $HOME/.pythonbrew/etc/bashrc ]] && source $HOME/.pythonbrew/etc/bashrc
```


## 三、使用Pythonbrew

```
1、查看可安装的Python版本
$ pythonbrew list --know

2、安装需要的Python版本，需要安装curl工具；安装会自动完成；
$ pythonbrew install 3.3.1

3、查看已经安装的Python版本，后面有*号表示正在使用的版本
$ pythonbrew list

4、选择一个python版本使用，只在当前终端有效
$ pythonbrew use 3.3.1

5、选择python3.3.1版本作为系统(用户)默认版本使用，会把该版本的路径添加到PATH中
$ pythonbrew switch 3.3.1


# ------------------------------------------------------------------------------------------------------------------------------------
Note: 本人按上述操作安装好pythonbrew之后，执行命令：pythonbrew switch 3.3.1 居然不能正确切换到指定的python版本上，后来发现原因是：
在安装pythonbrew完成之后，一定要在.bashrc文件中写入以下内容：
[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source "$HOME/.pythonbrew/etc/bashrc"
并且执行：source .bashrc
这样就可以正常切换到指定版本的python了。
# ------------------------------------------------------------------------------------------------------------------------------------

6、取消pythonbrew选择的版本
$ pythonbrew off

7、清理安装后的版本的源码和安装包
$ pythonbrew cleanup

8、指定Python版本运行文件
$ pythonbrew py -p 3.3.1 test.py

9、删除制定Python版本
$ pythonbrew uninstall 3.3.1
```