# -*- coding: utf-8 -*-
#

from collections import defaultdict
route_table = defaultdict(list)

def sub(topic, callback):
    if callback in route_table[topic]:
        return
    route_table[topic].append(callback)

def pub(topic, *a, **kw):
    for func in route_table[topic]:
        func(*a, **kw)

###########################
# 订阅者1
def oObserver1(name):
    print 'Hello, %s.' % name

# 订阅者2
def oObserver2(name):
    print 'Hello1, %s.' % name

# 订阅
sub('greet', oObserver1)
sub('greet', oObserver2)
sub('greet', oObserver2)

sub('abc', oObserver2)

# 发布
pub('greet', 'wwt')

pub('greet', '123')

# Hello, wwt.
# Hello1, wwt.

import tkMessageBox