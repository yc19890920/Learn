# -*- coding: utf-8 -*-

"""
无效地址库操作
"""

import re
from flask import request, jsonify
from flask import current_app
from bson.objectid import ObjectId

def search():
    """
    使用指定的关键字从无效地址池查找邮箱
    """
    data = {'count': 0, 'rows': []}
    key = request.args.get('key') or request.form.get('key')
    if not key:
        return jsonify(**data)
    key_list = map(lambda s: s.strip().lower(), key.split('\n'))
    mongodb = current_app.config.get('mongodb')
    mg_curs = mongodb['mm-mc'].badmail.find({'addr': {'$in': key_list}})
    data['count'] = mg_curs.count()
    for item in mg_curs:
        data['rows'].append({'id': str(item['_id']), 'addr': item['addr']})
    return jsonify(**data)


def delete():
    """
    从失败地址池删除指定邮箱
    """
    ids = request.args.get('ids') or request.form.get('ids')
    res = {'result': True}
    if not ids:
        return jsonify(**res)
    id_list = [ObjectId(s.strip()) for s in re.split('[,|\n]', ids) if len(s) == 24]
    if not id_list:
        return jsonify(**res)
    mongodb = current_app.config.get('mongodb')
    mongodb['mm-mc'].badmail.remove({'_id': {'$in': id_list}})
    return 'true'


def get_stat_info():
    """
    取得失败地址池统计信息
    """
    mongodb = current_app.config.get('mongodb')
    db = mongodb['mm-mc'].badmail
    name = db.name
    count = db.count()
    return jsonify(**{'name': name, 'count': count})

