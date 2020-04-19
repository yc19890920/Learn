# 用chardet判断字符编码的方法

## 安装
```pip install chardet```

## 实例
使用中，chardet.detect()返回字典，其中confidence是检测精确度，encoding是编码形式

- 网页编码判断
```
import urllib
import chardet
rawdata = urllib.urlopen('http://www.google.cn/').read()
res = chardet.detect(rawdata)
print res
# {'confidence': 0.98999999999999999, 'encoding': 'GB2312'}
```
- 文件编码判断
```
import chardet
with open('test.txt') as f:
    content = f.readlines()
res = chardet.detect(content)
print res
# {'confidence': 0.98999999999999999, 'encoding': 'GB2312'}
```



