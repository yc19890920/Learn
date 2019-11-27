# -*- coding: utf-8 -*- 
"""
author：     yangcheng
date：       2019/11/22 13:49
desc：

"""

import glob
from concurrent import futures

def find_robots(filename):
    '''
    Find all of the hosts that access robots.txt in a single log file

    '''
    robots = set()
    with open(filename, 'r') as f:
        for line in f.readlines():
            robots.add(line)
    return robots

def find_all_robots():
    '''
    Find all hosts across and entire sequence of files
    '''
    files = glob.glob('*.py')
    all_robots = set()
    with futures.ProcessPoolExecutor() as pool:
        for robots in pool.map(find_robots, files):
            all_robots.update(robots)
    return all_robots

if __name__ == '__main__':
    robots = find_all_robots()
    for ipaddr in robots:
        print(ipaddr)