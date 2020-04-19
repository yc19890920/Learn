# -*- coding: utf-8 -*-

import sys
import subprocess
from lib import _utils as Utils
from flask import current_app

jsonResponse = Utils.jsonResponse

def public_handle():
    """
    重启 HandleMails 服务
    """
    supervisor_cmd = Utils.get_supervisor_cmd()

    cmd = '{supervisor_cmd} restart public_handle'.format(supervisor_cmd=supervisor_cmd)
    print >> sys.stderr, 'cmd: {}'.format(cmd)
    res = subprocess.call(cmd, shell=True)
    if res == 0:
        return jsonResponse(True)
    else:
        return jsonResponse(False, 'execute_command_error')

def update_user(user_id, address=None):
    db_pool = current_app.config.get('db_pool')
    print >> sys.stderr, u'user_id: {}, address: {}'.format(user_id, address)
    sql = 'UPDATE core_customer SET address=%s WHERE customer_id=%s'
    print >> sys.stderr, 'sql: {}'.format(sql)
    args = (address, user_id)
    db_pool.do(sql, args)
    return jsonResponse(True)


