# -*- coding: utf-8 -*-
from .langconv import Converter

def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line)
    return line

def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line)
    return line