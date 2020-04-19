
# [python中常用的base64 md5 aes des crc32等的加密解密](http://www.cnblogs.com/darkpig/p/5676076.html) #

Python内置的base64模块可以实现base64、base32、base16、base85、urlsafe_base64的编码解码，python 3.x通常输入输出都是二进制形式，2.x可以是字符串形式。

**1. base64**

base64模块的base64编码、解码调用了binascii模块，binascii模块中的b2a_base64()函数用于base64编码，binascii模块中的a2b_base64()函数用于base64解码。
```
    >>>import base64
    >>> s = 'hello,word!'
    
    >>> base64.b64encode(s)    #base64编码，编码的字符串必须是二进制形式的
    b'aGVsbG8sd29yZCE='
    
    >>> base64.b64decode(b'aGVsbG8sd29yZCE=')    #base64解码
    b'hello,word!'
```

**2. md5**

Python2.x中有md5模块，此模块调用了hashlib模块，python3.x已中将md5取掉，直接通过调用hashlib模块来进行md5。Python2.x可以直接使用unicode字符，但3.x中必须使用二进制字节串。
```
    >>> import hashlib
    >>> m = hashlib.md5()
    >>> m.update(b'hello,word!')
    >>> m.hexdigest()
    '9702d6722a0901398efd4ecb3a20423f'
```
**注意：每调用一次update(s)，相当于给md5对象m增加了s。对一个新的需md5加密的内容，需要新建一个md5对象。**

**Hashlib模块还可以进行sha1、sha224、sha256、sha384、sha512等hash算法。Sha384、sha512在32位的平台上处理较慢。**


**3. crc32**

计算指定内容的crc32校验值，可以用zlib以及binascii模块的crc32函数.
```
>>> import zlib
>>> import binascii
s = b'hello,word!'
>>> zlib.crc32(s)
3035098857

>>> binascii.crc32(s)
3035098857
```

**4. crypt**
crypt 模块(只用于 Unix/Linux,windows平台上没有此模块)实现了单向的 DES 加密, Unix/Linx系统使用这个加密算法来储存密码，这个模块真正也就只在检查这样的密码时有用。
```
>>> import crypt
>>> import random
>>> import string
>>> chars = string.digits + string.letters
>>> chars
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> def getsalt(chars):
...     return random.choice(chars) + random.choice(chars)
... 
>>> salt = getsalt(chars)
>>> salt
'sb'
>>> msg = crypt.crypt('hello,world!',salt)  # 加盐
>>> msg
'sb0xvR6UbZsqw'
```

**5. 利用pycrypto包进行AES、DES、MD5等加密**

第三方Crypto包提供了较全面的加密算法，包括Cipher、Hash、Protocol、PublicKey、Singature、Util几个子模块，其中Cipher模块中有常用的AES、DES加密算法，Hash模块中有MD5、MD4、SHA等算法。

下面介绍AES及DES的加密解密算法。

- 5.1 AES加密解密

```
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto import Random
import binascii

key = '1234567890!@#$%^'   #秘钥，必须是16、24或32字节长度
iv = Random.new().read(16) #随机向量，必须是16字节长度

cipher1 = AES.new(key,AES.MODE_CFB,iv)  #密文生成器,MODE_CFB为加密模式

encrypt_msg =  iv + cipher1.encrypt('我是明文')  #附加上iv值是为了在解密时找到在加密时用到的随机iv
print '加密后的值为：',binascii.b2a_hex(encrypt_msg)   #将二进制密文转换为16机制显示


cipher2 = AES.new(key,AES.MODE_CFB,iv) #解密时必须重新创建新的密文生成器
decrypt_msg = cipher2.decrypt(encrypt_msg[16:]) #后十六位是真正的密文
print '解密后的值为：',decrypt_msg.decode('utf-8')
```

- 5.2 DES3加密解密

```
# coding=utf-8

from Crypto.Cipher import DES3
from Crypto import Random
import binascii

key = '1234567890!@#$%^'
iv = Random.new().read(8)  #iv值必须是8位
cipher1 = DES3.new(key,DES3.MODE_OFB,iv)  #密文生成器，采用MODE_OFB加密模式
encrypt_msg =  iv + cipher1.encrypt('我是明文必须是八')
#附加上iv值是为了在解密时找到在加密时用到的随机iv,加密的密文必须是八字节的整数倍，最后部分
#不足八字节的，需要补位
print '加密后的值为：',binascii.b2a_hex(encrypt_msg)   #将二进制密文转换为16进制显示


cipher2 = DES3.new(key,DES3.MODE_OFB,iv) #解密时必须重新创建新的密文生成器
decrypt_msg = cipher2.decrypt(encrypt_msg[8:]) #后八位是真正的密文
print '解密后的值为：',decrypt_msg
```
