# -*- coding: utf-8 -*-
"""
ssl 私钥生成，
加密导出私钥，
解密导入私钥，
私钥签名， http://www.tianwaihome.com/2015/03/m2crypto-x509.html
证书  http://www.111cn.net/phper/python/68321.htm

OpenSSL命令---pkcs8:  http://blog.csdn.net/as3luyuan123/article/details/16105435
http://o-u-u.com/?p=1630
pkcs1与pkcs8格式RSA私钥互相转换:  http://www.voidcn.com/article/p-wtvrauvj-dh.html


M2Crypto==0.26.2
"""
from __future__ import unicode_literals

try:
    import cStringIO as StringIO
except:
    import StringIO

import os
import time
import uuid
import subprocess
from M2Crypto import X509, EVP, RSA, ASN1, BIO, util

def genPrivKey():
    """ 生成私钥
    """
    bio=BIO.MemoryBuffer()
    rsa=RSA.gen_key(2048, 65537, lambda *arg:None)
    rsa.save_key_bio(bio, None)
    return bio.read_all()

def getPrivateKeySize(privkey):
    """ 查看私钥大小
    """
    try:
        key=EVP.load_key_string(privkey, util.no_passphrase_callback)
        return key.size() * 8
    except:
        return 2048

def genPubKey(privkey):
    """ 生成公钥
    """
    bio=BIO.MemoryBuffer(privkey)
    key=EVP.load_key_bio(bio, util.no_passphrase_callback)
    return key.get_rsa().as_pem()

def getPubkey(Pkey):
    return Pkey.get_rsa().as_pem()

def exportPrivKey(privkey, passwd=None):
    """ 获取导出加密key
    # sudo openssl pkcs8 -in key.pem -topk8 -v2 des3 -passout 123456 -out enckey.pem

    # 1. 将私钥转换成pkcs8文件
    a. 带密码
    sudo openssl pkcs8 -in  key.pem -topk8 -v2 des3 -inform PEM  -passout pass:123456 -out enckey1.pem
    b. 无密码
    sudo openssl pkcs8 -in  key.pem -topk8 -v2 des3 -inform PEM  -nocrypt -out enckey2.pem
    """
    # 校验是不是正确的key
    try:
        EVP.load_key_string(privkey)
    except EVP.EVPError as e:
        raise EVP.EVPError(e)
    except Exception as e:
        raise Exception(e)

    uuidstr = str(uuid.uuid1())
    privkeypath = "/tmp/private-key-{}.pem".format(uuidstr)
    enckeypath = "/tmp/encrypted-key-{}.pem".format(uuidstr)

    with open(privkeypath, 'wb') as f:
        f.write(privkey)

    if passwd:
        cmd = "sudo openssl pkcs8 -in {} -topk8 -v2 des3 -inform PEM  -passout pass:{} -out {}".format(privkeypath, passwd, enckeypath)
    else:
        cmd = "sudo openssl pkcs8 -in  {} -topk8 -v2 des3 -inform PEM  -nocrypt -out {}".format(privkeypath, enckeypath)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    if p.returncode ==0:
        with open(enckeypath, 'r') as f:
            enckey = f.read()

        os.unlink(privkeypath)
        os.unlink(enckeypath)
        return enckey
    raise Exception("Error read key")

def importPrivKey(enckey, passwd):
    """ 导入解密key

    # 2. 将pkcs8文件 转换成私钥
    PKCS8格式私钥转换为PKCS1
    1. 带密码
    sudo openssl pkcs8 -in enckey1.pem -inform PEM -passin pass:123456 -outform PEM -out pkey.pem

    2. 不带密码
    sudo openssl pkcs8 -in enckey2.pem -inform PEM -nocrypt -outform PEM -out pri_key.pem
    """
    uuidstr = str(uuid.uuid1())
    privkeypath = "/tmp/private-key-{}.pem".format(uuidstr)
    enckeypath = "/tmp/encrypted-key-{}.pem".format(uuidstr)
    with open(enckeypath, 'wb') as f:
        f.write(enckey)

    if passwd:
        cmd = "sudo openssl pkcs8 -in {} -inform PEM -passin pass:{} -outform PEM -out {}".format(enckeypath, passwd, privkeypath)
    else:
        cmd = "sudo openssl pkcs8 -in {} -inform PEM -nocrypt -outform PEM -out {}".format(enckeypath, privkeypath)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    if p.returncode ==0:
        with open(privkeypath, 'r') as f:
            privkey = f.read()

        os.unlink(privkeypath)
        os.unlink(enckeypath)
        return privkey
    raise Exception("Error decrypting key")

def genSignature(privkey, sig_domain="WangYang", sig_depart="", sig_organization="IIE", sig_province="Beijing", sig_locale="Beijing"):
    #首先载入密钥文件。此文件同时保存了申请者的私钥与公钥。
    pkey=EVP.load_key_string(privkey, util.no_passphrase_callback)
    req=X509.Request()
    req.set_pubkey(pkey) #包含公钥
    #req.set_version(1)

    #身份信息不是简单的字符串。而是X509_Name对象。
    name=X509.X509_Name()

    #CN是Common Name的意思。如果是一个网站的电子证书，就要写成网站的域名
    name.CN = sig_domain   # "WangYang"   # 普通名字

    #Organization Unit，通常是指部门吧，组织内单元
    name.OU = sig_depart   # "SKLOIS"

    #Organization。通常是指公司
    name.O = sig_organization # "IIE"

    #State or Province。州或者省
    name.ST = sig_province # "Beijing"

    #Locale。
    name.L = sig_locale # "Beijing"

    #国家。不能直接写国家名字，比如China之类的，而应该是国家代码。
    #CN代表中国。US代表美国，JP代表日本
    name.C="CN"  # 国家名称

    req.set_subject(name) #包含通信节点的身份信息
    req.sign(pkey, "sha256") #使用通信节点的密钥进行签名，sha1已经不安全了，这里使用sha256
    signature = req.as_pem()
    return signature

def getCertParm(obj):
    try:
        sig_domain = obj.CN
    except:
        sig_domain = ""

    try:
        sig_depart = obj.OU
    except:
        sig_depart = ""

    try:
        sig_organization = obj.O
    except:
        sig_organization = ""

    try:
        sig_province = obj.ST
    except:
        sig_province = ""

    try:
        sig_locale = obj.L
    except:
        sig_locale = ""

    try:
        sig_contry = obj.C
    except:
        sig_contry = ""
    return sig_domain, sig_depart, sig_organization, sig_province, sig_locale, sig_contry

def parseSignature(signature):
    if not signature:
        return "", "", "", "", ""
    try:
        # 返回一个X509.Request类型代表证书请求文件
        req=X509.load_request_string(signature)

        #首先验证一下，是不是真的是使用它本身的私钥签名的。
        #如果是，返回非0值。如果不是，说明这是一个非法的证书请求文件。
        is_verify = req.verify(req.get_pubkey())
        is_verify = is_verify and True or False
        S = req.get_subject()
        return is_verify, dict(zip(
            ("sig_domain", "sig_depart", "sig_organization", "sig_province", "sig_locale", "sig_contry"),
            getCertParm(S) )
        )
    except:
        return False , dict(zip(
            ("sig_domain", "sig_depart", "sig_organization", "sig_province", "sig_locale", "sig_contry" ),
            ( "", "", "", "", "", "" ) )
        )

def genCertificate(privkey, signature, certificate):
    #首先读取证书请求文件。
    # signature=file("req.pem", "rb").read()
    #返回一个X509.Request类型代表证书请求文件
    req=X509.load_request_string(signature)

    #首先验证一下，是不是真的是使用它本身的私钥签名的。
    #如果是，返回非0值。如果不是，说明这是一个非法的证书请求文件。
    is_verify = req.verify(req.get_pubkey())
    if not is_verify:
        return False, False, None

    #接下来载入CA的电子证书。与CA的密钥不一样，CA的电子证书包含了CA的身份信息。
    #CA的电子证书会分发给各个通信节点。
    # certificate=file("ca.pem", "rb").read()
    ca=X509.load_cert_string(certificate)

    #可以使用check_ca()方法判断这个证书文件是不是CA。
    #本质是判断它是不是自签名。如果是的话，就返回非0值。如果不是的话就返回0。
    is_ca = ca.check_ca()
    # if not is_ca:
    #     return True, False, None

    #接下来载入CA的密钥
    # cakey_str=file("cakey.pem", "rb").read()
    #一般CA的密钥要加密保存。回调函数返回密码
    # cakey=EVP.load_key_string(privkey, lambda *args: "1234")
    cakey=EVP.load_key_string(privkey, util.no_passphrase_callback)

    #接下来开始生成电子证书
    cert=X509.X509()

    #首先，设定开始生效时间与结束生效时间
    t = long(time.time()) + time.timezone #当前时间，单位是秒

    #开始生效时间。证书的时间类型不是普通的Python datetime类型。
    now = ASN1.ASN1_UTCTIME()
    now.set_time(t)
    nowPlusYear = ASN1.ASN1_UTCTIME() #结束生效时间
    nowPlusYear.set_time(t + 60 * 60 * 24 * 365) #一年以后。
    cert.set_not_before(now)
    cert.set_not_after(nowPlusYear)

    # 把证书请求附带的身份信息复制过来
    cert.set_subject(req.get_subject())

    #设置颁发者的身份信息，把CA电子证书内身份信息复制过来
    cert.set_issuer(ca.get_subject())

    #序列号是指，CA颁发的第几个电子证书文件
    cert.set_serial_number(2)

    #把证书请求内的公钥复制过来
    cert.set_pubkey(req.get_pubkey())

    #使用CA的秘钥进行签名。
    cert.sign(cakey, "sha1")

    certificateT = cert.as_pem()
    return True, True, certificateT
    #保存文件。
    file("cert.pem", "wb").write(cert.as_pem())

def parseCert(certificate):
    ca=X509.load_cert_string(certificate)
    S = ca.get_subject()
    I = ca.get_issuer()
    subject = dict(zip(
        ("sig_domain", "sig_depart", "sig_organization", "sig_province", "sig_locale", "sig_contry" ),
        getCertParm(S) )
    )
    issuer = dict(zip(
        ("sig_domain", "sig_depart", "sig_organization", "sig_province", "sig_locale", "sig_contry" ),
        getCertParm(I) )
    )
    return subject, issuer

def checkCert(privkey, certificate):
    pubkey1 = genPubKey(privkey)
    ca=X509.load_cert_string(certificate)
    pubkey2 = getPubkey(ca.get_pubkey())
    if pubkey1 == pubkey2:
        return True
    return False

if __name__ == "__main__":

    # import paramiko
    # ssh = paramiko.SSHClient()
    print '-----------privkey-------------------'
    privkey = genPrivKey()
    print privkey

    print '-----------pubkey-------------------'
    pubkey = genPubKey(privkey)
    print pubkey

    print '-------------size-----------------'
    size = getPrivateKeySize(privkey)
    print size

    print '-------------exportprivkey-----------------'
    privkey = exportPrivKey(privkey, "123456")
    print privkey

    print '-------------importprivkey-----------------'
    privkey = importPrivKey(privkey, "123456")
    print privkey

    print '-------------signature-----------------'
    signature = genSignature(privkey)
    print signature

    print '-------------parseSignature-----------------'
    print parseSignature(signature)

