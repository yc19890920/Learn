# -*- coding: utf-8 -*-

import hashlib
import datetime
from flask import request, current_app, jsonify

def validate_key():
    """
    安全认证：查看客户端key和服务器端key是否相同
    """
    auth_key = current_app.config.get('auth_key')
    auth_string = request.args.get('auth', '')
    auth_string_server = hashlib.md5('%s-%s' % (auth_key, datetime.datetime.now().strftime("%Y%m%d"))).hexdigest()
    return True if auth_string == auth_string_server else False

def jsonResponse(status, data='', **kwargs):
    """
    输出返回信息
    """
    res = {'status': status}
    if data:
        res['data'] = data
    res.update(kwargs)
    return jsonify(res)

def get_supervisor_cmd():
    config = current_app.config
    # ctl_cmd = os.path.join(os.path.dirname(sys.executable), 'supervisorctl')
    ctl_cmd = config.get('supervisorctl')
    conf_file = config.get('supervisor_conf_file')
    cmd = '{ctl_cmd} -c {conf_file}'.format(ctl_cmd=ctl_cmd, conf_file=conf_file)
    return cmd


