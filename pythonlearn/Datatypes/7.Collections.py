# -*- coding: utf-8 -*-

'''
collections模块包含了内建类型之外的一些有用的工具，例如Counter、defaultdict、OrderedDict、deque以及nametuple。
其中Counter、deque以及defaultdict是最常用的类。
'''

import re
from collections import Counter


def find_frequency_word():
    string = """   Lorem ipsum dolor sit amet, consectetur
    adipiscing elit. Nunc ut elit id mi ultricies
    adipiscing. Nulla facilisi. Praesent pulvinar,
    sapien vel feugiat vestibulum, nulla dui pretium orci,
    non ultricies elit lacus quis ante. Lorem ipsum dolor
    sit amet, consectetur adipiscing elit. Aliquam
    pretium ullamcorper urna quis iaculis. Etiam ac massa
    sed turpis tempor luctus. Curabitur sed nibh eu elit
    mollis congue. Praesent ipsum diam, consectetur vitae
    ornare a, aliquam a nunc. In id magna pellentesque
    tellus posuere adipiscing. Sed non mi metus, at lacinia
    augue. Sed magna nisi, ornare in mollis in, mollis
    sed nunc. Etiam at justo in leo congue mollis.
    Nullam in neque eget metus hendrerit scelerisque
    eu non enim. Ut malesuada lacus eu nulla bibendum
    id euismod urna sodales.  """
    words = re.findall(r'\w+', string) #This finds words in the document
    lower_words = [word.lower() for word in words] #lower all the words
    word_counts = Counter(lower_words) #counts the number each time a word appears
    print word_counts
    '''
    Counter({
    'elit': 5, 'sed': 5, 'in': 5,
    'adipiscing': 4, 'mollis': 4, 'eu': 3, 'id': 3, 'nunc': 3, 'consectetur': 3, 'non': 3, 'ipsum': 3,
    'nulla': 3, 'pretium': 2, 'lacus': 2, 'ornare': 2, 'at': 2, 'praesent': 2, 'quis': 2, 'sit': 2,
    'congue': 2, 'amet': 2, 'etiam': 2, 'urna': 2, 'a': 2, 'magna': 2, 'lorem': 2, 'aliquam': 2, 'ut': 2,
    'ultricies': 2, 'mi': 2, 'dolor': 2, 'metus': 2, 'ac': 1, 'bibendum': 1, 'posuere': 1, 'enim': 1,
    'ante': 1, 'sodales': 1, 'tellus': 1, 'vitae': 1, 'dui': 1, 'diam': 1, 'pellentesque': 1, 'massa': 1,
    'vel': 1, 'nullam': 1, 'feugiat': 1, 'luctus': 1, 'pulvinar': 1, 'iaculis': 1, 'hendrerit': 1, 'orci': 1,
    'turpis': 1, 'nibh': 1, 'scelerisque': 1, 'ullamcorper': 1, 'eget': 1, 'neque': 1, 'euismod': 1, 'curabitur': 1,
    'leo': 1, 'sapien': 1, 'facilisi': 1, 'vestibulum': 1, 'nisi': 1, 'justo': 1, 'augue': 1,
    'tempor': 1, 'lacinia': 1, 'malesuada': 1
    })
    '''
    print dict(word_counts) # 打印字典



if __name__ == "__main__":
    # ------------Counter----------------
    # 如果你想统计一个单词在给定的序列中一共出现了多少次，诸如此类的操作就可以用到Counter。
    # 来看看如何统计一个list中出现的item次数
    li = ["Dog", "Cat", "Mouse", 42, "Dog", 42, "Cat", "Dog"]
    a = Counter(li)
    print a
    # Counter({'Dog': 3, 42: 2, 'Cat': 2, 'Mouse': 1})

    # 中不同单词的数目
    print len(set(li)) # 4

    # 对结果进行分组
    print "{0} : {1}".format(a.values(),a.keys())  # [1, 3, 2] : ['Mouse', 'Dog', 'Cat']

    # 获取最多的3个
    print(a.most_common(3)) # [('Dog', 3), ('Cat', 2), ('Mouse', 1)]


    # 文本找出单词的频率
    find_frequency_word()


