# -*- coding: UTF-8 -*-

import time
import traceback

try:
    from pymongo import MongoClient
except ImportError:
    import warnings
    warnings.warn("Strongly recommend upgrading to the latest version pymongo version,"
                  "Connection is DEPRECATED: Please use mongo_client instead.")
    from pymongo import Connection as MongoClient

class Mongo(object):

    def __init__(self, param, logger):
        self.param = param
        self.logger = logger
        self._conn = MongoClient(self.param['mongo']['host'], int(self.param['mongo']['port']))

    def init(self, outerr=True):
        try:
            self.__mongodb = self._conn[self.param['mongo']['dbname']]
            self.__mongodb.authenticate(self.param['mongo']['user'], self.param['mongo']['pass'])
        except Exception as e:
            if outerr:
                self.logger.error(u'init mongodb connect exception')
                self.logger.error(traceback.format_exc())
            return False
        self.logger.info(u'init mongodb connect success.')
        return True

    # 取得 MongoDB 的 Collection 对象
    def get_collection(self, c_name='badmail'):
        return self.__mongodb[c_name]

    # 维护 MongoDB 连接
    def maintain_mongodb(self, trycount=5) :
        i = 0
        while not self.init():
            self.logger.error(u'try connect mongodb: {}'.format(i+1))
            i += 1
            if i == trycount :
                self.logger.error(u'reconnect mongodb failure\n{}'.format(traceback.format_exc()))
                return False
            time.sleep(3)
        self.logger.info(u'reconnect mongodb success.')
        return True

    def dispose(self):
        self._conn.close()
        self.logger.info(u'close mongodb connect success.')
