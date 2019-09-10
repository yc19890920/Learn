蓝灯 免费代理

- [Shadowsocks配置文件，蓝灯(Lantern)破解，手机版+win版](https://github.com/ntkernel/lantern)
- [蓝灯Windows下载](https://github.com/getlantern/download)
- [蓝灯](https://getlantern.org/zh_CN/)

go proxy 免费高匿代理抓取
- [go proxy 免费高匿代理抓取](https://studygolang.com/topics/6078)

export GOROOT=/usr/local/go
export GOPATH=/home/python/gocode
export PATH=$PATH:$GOPATH:/usr/local/go/bin
写入： .bashrc 

source .bashrc 


Version 2.0
不再依赖 MySQL 和 NSQ！
之前需要分别启动publisher、consumer和assessor，现在 只需要启动主程序 即可！
提供了高度灵活的 API 接口，在启动主程序后，即可通过在浏览器访问localhost:9999/all 与 localhost:9999/random 直接获取抓到的代理！
甚至可以使用 localhost:9999/sql?query=来执行 SQL 语句来自定义代理筛选规则！
提供 Windows、Linux、Mac 开箱即用版！ Download Release v2.0

1. 通过编译源码
go get github.com/storyicon/golang-proxy
进入到 golang-proxy 目录，执行 go build main.go，执行生成的二进制的执行程序即可。

注意： 在 go build 的过程中可能出现cannot find package "github.com/gocolly/col1ly" in any of 等找不到包的情况，根据提示的地址 go get 即可

# 比如如果在 go build main.go 的时候提示
business\publisher.go:8:2: cannot find package "github.com/gocolly/col1ly" in any of:
        F:\Go\src\github.com\gocolly\col1ly (from $GOROOT)
        D:\golang\src\github.com\gocolly\col1ly (from $GOPATH)
        C:\Users\Administrator\go\src\github.com\gocolly\col1ly
        D:\ivank\src\github.com\gocolly\col1ly
执行 go get github.com/gocolly/col1ly 即可
如果觉得麻烦，可以使用 /bin 目录中提供的 开箱即用 版本。

