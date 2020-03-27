# -*- coding: utf-8 -*-

def replace_withstrip(word, replace="\n", replace_to="", strip=True):
    if isinstance(word, (basestring, str)):
        word = word.replace(replace, replace_to)
        word = word.strip()
    return word