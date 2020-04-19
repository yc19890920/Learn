# -*- coding: utf-8 -*-
#
import os
import shutil

# 删除目录列表，或者文件列表
def remove_dir_file(path_list=None):
    path_list = path_list if isinstance(path_list, (list, tuple)) else [path_list]
    for path in path_list:
        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, True)
    return True

# 创建指定的多个路径
def make_dir(path_list, mode=0755):
    if type(path_list) == type(''): path_list = [path_list]
    for path in path_list:
        if os.path.exists(path): continue
        recursion_make_dir(path, mode)
    return True

# 递归创建路径
def recursion_make_dir(path, mode=0755):
    if path[0] != '/': return False
    path_list = os.path.realpath(path).split('/')[1:]
    path_full = ''
    for i in path_list:
        path_full += '/' + i
        if os.path.exists(path_full): continue
        os.mkdir(path_full, mode)
    return True