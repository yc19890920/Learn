# -*- coding: utf-8 -*-

import gevent.monkey
import gevent.pywsgi
gevent.monkey.patch_all()

import os
from flask import Flask, abort, request

from lib import (
    _settings as Settings,
    _dbkit as DBkit,
    _utils as Utils,
)
from actions import (
    _supervisor as Supervisor,
    _mongo as Mongo
)

ROOT = os.path.realpath(os.path.dirname(__file__))
redis = DBkit.get_redis_connection(Settings.REDIS_SET)
mongodb = DBkit.getDBObject(creater='mongo', dbtype='mongo', params=Settings.DATABASES['mongo']['mongo'])
db_pool = DBkit.getDBObject(creater='mysql', dbtype='edm_web', params=Settings.DATABASES['mysql']['edm_web'])

app = Flask(__name__)
app.config.update({
    'DEBUG': Settings.DEBUG,
    'ROOT': ROOT,
    'supervisorctl': Settings.SUPERVISORCTL,
    'supervisor_conf_file': Settings.SUPERVISOR_CONF_FILE,
    'auth_key': Settings.AUTH_KEY,
    'redis': redis,
    'mongodb': mongodb,
    'db_pool': db_pool
})

jsonResponse = Utils.jsonResponse


@app.errorhandler(401)
def page_not_found(e):
    return jsonResponse(False, 'auth_error')

@app.route('/api', methods=['GET', 'POST'])
def api_actions():
    if not Utils.validate_key():
        raise abort(401)
    action = request.args.get('action', '')
    if action == 'public-handle':
        return Supervisor.public_handle()
    if action == 'update-customer':
        user_id = request.args.get('user_id', None) or request.form.get('user_id', None)
        address = request.args.get('address', None) or request.form.get('address', None)
        return Supervisor.update_user(user_id, address)
    return jsonResponse(False, 'auth_error')


@app.route('/mongo', methods=['POST', 'GET'])
def mongo_actions():
    if not Utils.validate_key():
        raise abort(401)
    action = request.args.get('action', '')
    if action == 'search':
        return Mongo.search()
    if action == 'delete':
        return Mongo.delete()
    if action == 'get-stat-info':
        return Mongo.get_stat_info()
    return Mongo(False, 'param_error')


if __name__ == '__main__':
    s = gevent.pywsgi.WSGIServer( (Settings.LISTEN_IP, Settings.LISTEN_PORT), app )
    s.serve_forever()
    # app.run(host=listen_ip, port=listen_port)

