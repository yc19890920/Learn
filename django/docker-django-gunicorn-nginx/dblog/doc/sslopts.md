## 创建一个自签名的 SSL 证书 


    #### 使用 OpenSSL 创建自签名证书


    ## 1.创建根证书的私钥
    openssl genrsa -out ca.key 1024

    ## 2.使用私钥创建根证书
    openssl req -new -x509 -days 36500 -key ca.key -out ca.crt -subj "/C=CN/ST=Fujian/L=Xiamen/O=Your Company Name/OU=Your Root CA"
    openssl req -new -x509 -days 36500 -key ca.key -out ca.crt -subj "/C=CN/ST=Guangdong/L=ShenZhen/O=Test Company/OU=Computer Department"

    ## 3.创建服务器私钥
    openssl genrsa -out server.key 1024

    ## 4.使用服务器私钥创建证书请求文件
    openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Fujian/L=Xiamen/O=Your Company Name/OU=youwebsite.org/CN=yourwebsite.org"
    openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Guangdong/L=ShenZhen/O=Test Company/OU=djangoblog.com/CN=djangoblog.com"

    ## 5.准备工作
    mkdir -p demoCA/newcerts
    touch demoCA/index.txt
    echo '01' > demoCA/serial

    ## 6.创建服务器证书并使用ca根证书签名
    openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key


    ## ---查看不同格式文件的内容命令语法
    # openssl rsa -noout -text -in ca.key
    # openssl x509 -noout -text -in ca.crt
    # openssl rsa -noout -text -in server.key
    # openssl req -noout -text -in server.csr
    # openssl x509 -noout -text -in server.crt

    ## 创建证书最简单方式
    # openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.key

