# coding: utf-8



teamitems = [
    {'team':'France'      , 'P':1 , 'GD':-3 , 'GS':1 , 'GA':4},
    {'team':'Uruguay'     , 'P':7 , 'GD':4  , 'GS':4 , 'GA':0},
    {'team':'SouthAfrica', 'P':4 , 'GD':-2 , 'GS':3 , 'GA':5},
    {'team':'Mexico'      , 'P':4 , 'GD':1  , 'GS':3 , 'GA':2}
]

# 1. lambda 多列排序
s = sorted(teamitems, key=lambda x: ( x['GA'], x['GD'], x['GS'], ['P'] ), reverse=True)
print s
# [{'P': 4, 'GD': -2, 'GS': 3, 'GA': 5, 'team': 'SouthAfrica'}, {'P': 1, 'GD': -3, 'GS': 1, 'GA': 4, 'team': 'France'}, {'P': 4, 'GD': 1, 'GS': 3, 'GA': 2, 'team': 'Mexico'}, {'P': 7, 'GD': 4, 'GS': 4, 'GA': 0, 'team': 'Uruguay'}]


# 不过这样一个个取字典的键值有点啰嗦，用itemgetter更简洁优雅,上面那句代码可以用如下替换。 取域
from operator import itemgetter

s = sorted(teamitems, key=itemgetter( 'P', 'GD'), reverse=True)
print s
# [{'P': 7, 'GD': 4, 'GS': 4, 'GA': 0, 'team': 'Uruguay'}, {'P': 4, 'GD': 1, 'GS': 3, 'GA': 2, 'team': 'Mexico'}, {'P': 4, 'GD': -2, 'GS': 3, 'GA': 5, 'team': 'SouthAfrica'}, {'P': 1, 'GD': -3, 'GS': 1, 'GA': 4, 'team': 'France'}]