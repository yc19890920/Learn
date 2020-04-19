# -*- coding: utf-8 -*-

'''

# 实现多层次嵌套结构
data = [
    # user_id, task_name, domain, success, err_1, err_2, err_3
    (2369, '201708091111-2369-20', 'qq.com', 100, 1, 2, 15),
    (2369, '201708091111-2369-20', '163.com', 120, 1, 2, 17),
    (3469, '201708091113-3469-28', 'qq.com', 300, 10, 50, 100),
    (2555, '201708091113-2555-28', '*', 180, 10, 10, 0),
]
output:
{
    user_id1: {
        task_name1:{
            domain1: {
                'success': 0,
                'err_1': 0,
                'err_2': 0,
                'err_3': 0,
            }
        },
        task_name2:{
            ...
        },
        ...
    },
    user_id2: {
        task_name3:{
            domain3: {
                ...
            },
            ...
        },
        task_name3:{
            ...
        },
        ...
    },
    ...
}

'''
# 数据
data = [
    # user_id, task_name, domain, success, err_1, err_2, err_3
    (2369, '201708091111-2369-20', 'qq.com', 100, 1, 2, 15),
    (2369, '201708091111-2369-20', 'qq.com', 500, 1, 0, 15),
    (2369, '201708091111-2369-20', '163.com', 120, 1, 2, 17),
    (2369, '201708101111-2369-20', '163.com', 150, 1, 2, 17),
    (3469, '201708091113-3469-28', 'qq.com', 300, 10, 50, 100),
    (2555, '201708091113-2555-28', '*', 180, 10, 10, 0),
]

import pprint

############################################################

# 可以设计一个继承了dict的类，实现的方法也很是简单，
# 只要使用__getitem__魔法函数就可以模拟友好的字典。

class MagicDict(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

mgicD = MagicDict()

for res in data:
    user_id, task_name, domain, success, err_1, err_2, err_3 = res
    _D = mgicD[user_id][task_name][domain]
    _D['success'] = _D.get('success', 0) + success
    _D['err_1'] = _D.get('err_1', 0) + err_1
    _D['err_2'] = _D.get('err_2', 0) + err_2
    _D['err_3'] = _D.get('err_3', 0) + err_3

pprint.pprint(
    mgicD
)

# {
#     2369: {
#         '201708091111-2369-20': {
#             '163.com': {
#                 'err_1': 1,
#                 'err_2': 2,
#                 'err_3': 17,
#                 'success': 120
#             },
#             'qq.com': {
#                 'err_1': 1,
#                 'err_2': 2,
#                 'err_3': 15,
#                 'success': 100
#             }
#         },
#         '201708101111-2369-20': {
#             '163.com': {'err_1': 1, 'err_2': 2, 'err_3': 17, 'success': 150}}
#     },
#     2555: {'201708091113-2555-28': {'*': {'err_1': 10, 'err_2': 10, 'err_3': 0,  'success': 180}}},
#     3469: {'201708091113-3469-28': {'qq.com': {'err_1': 10, 'err_2': 50,  'err_3': 100, 'success': 300}}}
# }

############################################################
# Python可以采用非常巧妙的lambda结构来实现多层嵌套字典
# 无比神奇的lambda函数，可以将自己再作为函数无限嵌套，这样就非常容易实现多层嵌套的字典，并且随时可以引用增加数据。

from collections import defaultdict

_nested_dict = lambda: defaultdict(_nested_dict)
nestedD = _nested_dict()

for res in data:
    user_id, task_name, domain, success, err_1, err_2, err_3 = res
    _D = nestedD[user_id][task_name][domain]
    _D['success'] = _D.get('success', 0) + success
    _D['err_1'] = _D.get('err_1', 0) + err_1
    _D['err_2'] = _D.get('err_2', 0) + err_2
    _D['err_3'] = _D.get('err_3', 0) + err_3

print nestedD[2369]['201708091111-2369-20']['163.com']['success']

pprint.pprint(
    nestedD
)
# defaultdict(<function <lambda> at 0x0000000003049358>,
#                  { 2369: defaultdict(<function <lambda> at 0x0000000003049358>,
#                                                       {
#                                                       '201708091111-2369-20': defaultdict(<function <lambda> at 0x0000000003049358>,
#                                                                                                            {
#                                                                                                            'qq.com': defaultdict(<function <lambda> at 0x0000000003049358>, {'err_1': 1, 'err_3': 15, 'success': 100, 'err_2': 2}),
#                                                                                                             '163.com': defaultdict(<function <lambda> at 0x0000000003049358>, {'err_1': 1, 'err_3': 17, 'success': 120, 'err_2': 2})}),
#                                                     '201708101111-2369-20': defaultdict(<function <lambda> at 0x0000000003049358>, {'163.com': defaultdict(<function <lambda> at 0x0000000003049358>, {'err_1': 1, 'err_3': 17, 'success': 150, 'err_2': 2})})}),
#                    2555: defaultdict(<function <lambda> at 0x0000000003049358>, {'201708091113-2555-28': defaultdict(<function <lambda> at 0x0000000003049358>, {'*': defaultdict(<function <lambda> at 0x0000000003049358>, {'err_1': 10, 'err_3': 0, 'success': 180, 'err_2': 10})})}), 3469: defaultdict(<function <lambda> at 0x0000000003049358>, {'201708091113-3469-28': defaultdict(<function <lambda> at 0x0000000003049358>, {'qq.com': defaultdict(<function <lambda> at 0x0000000003049358>, {'err_1': 10, 'err_3': 100, 'success': 300, 'err_2': 50})})})
#                 }
# )

T2 = _nested_dict()

T2[1][2][3] = [5, 6, 7]

pprint.pprint(
    T2
)



