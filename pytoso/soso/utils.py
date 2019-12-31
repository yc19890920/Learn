import os
from soso.lib import utils

def add(x, y):
    print("--------soso")
    with open(os.path.join(os.path.dirname(__file__), "a.txt"), 'rb') as f:
        lines = f.readlines()
    print("lines", lines)
    return utils.add(x,y)