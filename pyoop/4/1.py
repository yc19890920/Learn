
class Mdict(dict):

    def __setattr__(self, key, value):
        if isinstance(value, (dict, Mdict)):
            value = Mdict(value)
        self.__dict__[key] = value

a = Mdict()

import collections.abc
import io

from collections import defaultdict

_nested_dict = lambda: defaultdict(_nested_dict)
nestedD = _nested_dict()