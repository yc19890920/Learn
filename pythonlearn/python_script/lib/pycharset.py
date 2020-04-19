# -*- coding: utf-8 -*-
#


### 解码 ###
# str -> utf8 或者其他
# 将字符串解码成 utf8
# 把utf-8编码表示的字符串'xxx'转换为Unicode字符串u'xxx'用decode('utf-8')
def character_decode(s, charset=None, errors=None):
    # replace, ignore
    errors = errors if errors else 'replace'
    if charset is not None:
        try:
            return s.decode(charset, errors)
        except Exception:
            return s.decode('utf-8', errors)
    else:
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return s.decode('gb18030')
            except UnicodeDecodeError:
                return s.decode('utf-8', errors)

### 编码 ###
# utf8 -> 其他
# 将utf8字符串解码成 其他
# 把u'xxx'转换为utf-8编码的'xxx'或其他编码的'xxx', 用decode('utf-8')或decode('其他')
def character_encode(s, charset=None, errors=None):
    # replace, ignore
    errors = errors if errors else 'replace'
    if charset is not None:
        try:
            return s.encode(charset, errors)
        except Exception:
            return s.encode('utf-8', errors)
    else:
        try:
            return s.encode('utf-8')
        except UnicodeEncodeError:
            try:
                return s.encode('gb18030')
            except UnicodeEncodeError:
                return s.encode('utf-8', errors)


def reload_decode(s, charset=None, errors=None):
    # replace, ignore
    errors = errors if errors else 'replace'
    try:
        s = character_decode(s, charset, errors)
    except:
        s = character_encode(s, charset, errors).decode('utf-8')
    return s
