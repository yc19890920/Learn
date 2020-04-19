# -*- coding: utf-8 -*-
#
from gevent import monkey
monkey.patch_all()

import gevent
import gevent.pool

import os
import sys
import re
import csv
import chardet
import xlrd
import time
import random
import traceback
import redis
import logging
import logging.handlers

from lib import pyetc, pidfile, zfile, pycharset, file_utils, common
from db import MongoPool, MysqlPool

signal_stop = False
log = None
mysql_pool = None
mongo_cn = None

fp_err_t1 = None
fp_err_t2 = None

# 正则表达式
self_phone_pattern = re.compile(r'((\+?86)|(\(\+86\)))?(\s)?(13[012356789][0-9]{8}|15[012356789][0-9]{8}|18[02356789][0-9]{8}|14[57][0-9]{8}|1349[0-9]{7}|177[0-9]{8})')
self_mail_pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+$')
self_var_pattern = re.compile('var\d+')

# 模块路径
ROOT = os.path.realpath(os.path.join(os.path.split(__file__)[0]))

ERR_ADDR_PATH = os.path.join(ROOT, 'data')
COMMON_VAR_COUNT_HASH = 'common_var_count_hash'
EDM_WEB_MAIL_IMPORT_ERROR_QUEUE = 'edm_web_mail_import_error_queque'

# 统计客户地址池数量队列（python 专用）
EDM_WEB_USER_MAIL_IMPORT_COUNT_QUEUE = 'edm_web_user_mail_import_count_queue'

# 无效地址后缀（雅虎）
FILTER_VALID_DOMAIN = (u'yahoo.com.cn', u'yahoo.cn')

redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.StrictRedis(connection_pool=redis_pool)

# ###########################################################
# 处理器
class Processor(object):

    def __init__(self, task, msg, file_extension, work_table, line, index):
        self.task = task
        self.customer_id = self.task['user_id']
        self.maillist_id = self.task['list_id']
        self.import_id = self.task['import_id']
        self.msg = '{}, index:{}'.format(msg, index+1)
        self.file_extension = file_extension
        self.work_table = work_table
        self.line = line

    # 处理异常
    def process_mongo_exception(self):
        return mongo_cn.maintain_mongodb()

    # 处理导入
    def run(self):
        # 初始化变量
        count_all  = 0
        count_err_1 = 0
        count_err_2 = 0
        time_import = time.strftime("%Y-%m-%d %H:%M:%S")
        mongo_cr = mongo_cn.get_collection()
        database_fields = self.get_database_fields()
        # 导入处理
        for line in self.line:
            if self.file_extension == 'txt':
                line = pycharset.reload_decode(line, None, 'replace')
                line_list = line.strip().replace(u'，', '\t').replace(',', '\t').replace(u'；', '\t').replace(';', '\t').split('\t')
            elif self.file_extension == 'csv':
                line_list = [pycharset.reload_decode(each, None, 'replace') for each in line]
            elif self.file_extension in ['xls', 'xlsx']:
                line_list = [pycharset.reload_decode(each, None, 'replace') for each in self.work_table.row_values(line)]
            addr = line_list[0].strip().lower()

            if not addr or addr == u'邮件地址':
                continue

            # 输出地址处理数量
            count_all += 1
            if count_all % 5000 == 0:
                log.info(u'{}. process count:{}'.format(self.msg, count_all))

            # 检测邮件地址格式
            if not self.check_format(addr):
                self.save_error_addr(fp_err_t1, addr)
                count_err_1 += 1
                continue

            # 去掉无效地址
            if addr.split('@')[-1] in FILTER_VALID_DOMAIN:
                self.save_error_addr(fp_err_t1, addr)
                count_err_1 += 1
                continue

            # 检测邮件地址有效性
            try:
                res = self.check_validity(mongo_cr, addr)
            except:
                mongo_cr = self.process_mongo_exception()
                if not mongo_cr:
                    continue
                res = self.check_validity(mongo_cr, addr)
            if not res:
                self.save_error_addr(fp_err_t1, addr)
                count_err_1 += 1
                continue

            # 获取各字段内容
            try :
                field = self.get_line_fields(addr, line_list)
            except Exception, e :
                log.error(u'{}. get fields data exception\n{}'.format(self.msg, traceback.format_exc()))
                count_all -= 1
                continue

            # 检测是否已存在当前邮件地址
            try :
                is_exist = self.check_exists(addr)
            except Exception, e:
                log.error(traceback.format_exc())
                is_exist = time_call(self.check_exists, addr)

            sql_parts, sql_args = self.get_fields_args(database_fields, field['var'])
            if is_exist:
                # 更新邮件地址
                try :
                    res = self.update_address(field, sql_parts, sql_args)
                except Exception, e :
                    log.error(traceback.format_exc())
                    res = time_call(self.update_address,  field, sql_parts, sql_args)
                    if not res:
                        pass
                self.save_error_addr(fp_err_t2, addr)
                count_err_2 += 1
            else:
                try :
                    res = self.insert_address(field, sql_parts, sql_args)
                except Exception, e :
                    log.error(traceback.format_exc())
                    res = time_call(self.insert_address,  field, sql_parts, sql_args)

        vals = {'count_all': count_all, 'count_err_1': count_err_1, 'count_err_2': count_err_2, 'time_import': time_import}
        try :
            save_res = self.set_result(vals)
        except Exception, e:
            log.error(traceback.format_exc())
            res = time_call(self.set_result,  vals)

        try :
            update_res = self.update_ml_maillist(vals)
        except Exception, e:
            log.error(traceback.format_exc())
            update_res = time_call(self.update_ml_maillist,  vals)

        log.info(u'{}. process finish, count:{} (e1:{}, e2:{})'.format(self.msg, count_all, count_err_1, count_err_2))
        return

    # 获取数据库字段名
    def get_database_fields(self):
        sql = "SELECT column_name FROM information_schema.COLUMNS WHERE table_name = 'ml_subscriber_{}' AND table_schema = 'mm-pool';".format(self.customer_id)
        res = mysql_pool.getAll(sql)
        return sorted(filter(lambda s: self_var_pattern.match(s), [r[0] for r in res]), key=lambda k: int(k[3:]))

    # 检测邮件地址是否已存在
    def check_exists(self, addr):
        sql = "SELECT address_id FROM `mm-pool`.`ml_subscriber_%s` WHERE list_id='%s' AND address=%s"
        args = (self.customer_id, self.maillist_id, addr)
        return mysql_pool.getOne(sql, args)

    # 设置任务结果
    def set_result(self, vals):
        sql = "UPDATE ml_import SET time_import=%s, time_finish=%s, count_all=count_all+%s, count_err_1=count_err_1+%s, count_err_2=count_err_2+%s WHERE id=%s"
        args = (vals['time_import'], time.strftime("%Y-%m-%d %H:%M:%S"), vals['count_all'], vals['count_err_1'], vals['count_err_2'], self.import_id)
        return mysql_pool.update(sql, args)

    # 更新无效地址率
    def update_ml_maillist(self, vals):
        sql = "UPDATE ml_maillist SET count_all=count_all+%s, count_err=count_err+%s WHERE list_id=%s"
        args = (vals['count_all']-vals['count_err_2'], vals['count_err_1'], self.maillist_id)
        return mysql_pool.update(sql, args)

    # 更新邮件地址
    def update_address(self, field, sql_parts, sql_args):
        sql = "UPDATE `mm-pool`.`ml_subscriber_%s` SET fullname=%s, sex=%s, birthday=%s, phone=%s, area=%s, created=%s{} WHERE list_id=%s AND address=%s".format(sql_parts)
        args = [self.customer_id, field['name'], field['sex'], field['birthday'], field['phone'], field['area'], time.strftime("%Y-%m-%d %H:%M:%S")] + sql_args + [self.maillist_id, field['addr']]
        return mysql_pool.update(sql, args)

    # 添加邮件地址
    def insert_address(self, field, sql_parts, sql_args):
        sql  = "INSERT INTO `mm-pool`.`ml_subscriber_%s` SET list_id=%s, address=%s, fullname=%s, sex=%s, birthday=%s, phone=%s, area=%s, created=%s{}".format(sql_parts)
        args = [self.customer_id, self.maillist_id, field['addr'], field['name'], field['sex'], field['birthday'], field['phone'], field['area'], time.strftime("%Y-%m-%d %H:%M:%S")] + sql_args
        return mysql_pool.update(sql, args)

    # 分解行数据中的各字段
    def get_line_fields(self, addr, line_list) :
        # 初始化字段
        field = {}
        field['addr'] = addr

        # 从读取的行中分解出各字段
        elen = len(line_list)
        field['name'] = line_list[1].strip() if elen >1 else addr.split('@')[0]

        sex = line_list[2].strip() if elen >2 else ''
        sex = self.analyze_gender(sex)

        birthday = line_list[3].strip() if elen >3 else ''
        birthday = self.analyze_birthday(birthday)

        phone = line_list[4].strip() if elen >4 else ''
        m = self_phone_pattern.search(phone)
        phone = m.group() if m else ''

        field['sex'] = sex
        field['birthday'] = birthday
        field['phone'] = phone
        field['area'] = line_list[5].strip() if elen >5 else ''

        field['var'] = line_list[6:]
        return field

    def get_fields_args(self, database_fields, field):
        process_len = min(len(database_fields), len(field))
        sql_part = "=%s,".join(database_fields[:process_len])
        if sql_part:
            sql_part = ',' + sql_part + "=%s"
        args = field[:process_len]
        return sql_part, args

    # 保存错误地址
    def save_error_addr(self, fw, addr):
        fw.write((pycharset.character_encode(addr))+'\r\n')
        return True

    # 检测邮件地址格式
    def check_format(self, addr):
        m = self_mail_pattern.search(addr)
        if m is None:
            return False
        return True

    # 检测邮件地址是否有效 (不在无效地址库中)
    def check_validity(self, cr, addr):
        if cr.find_one({"addr": addr}):
            return False
        return True

    # 判断性别
    def analyze_gender(self, sex):
        if sex in (u'男', u'M'):
            sex = u'M'
        elif sex in (u'女', u'F'):
            sex = u'F'
        else:
            sex = ''
        return sex

    # 分析日期
    def analyze_birthday(self, birthday):
        if not birthday:
            return '0000-00-00'
        try:
            birthday = int(float(birthday))
        except:
            birthday = birthday
        try:
            # excel
            birthday = xlrd.xldate.xldate_as_datetime(birthday, 0).strftime('%Y-%m-%d')
        except:
            # csv/txt
            flag = False
            for type in ["%Y/%m/%d", "%Y-%m-%d", "%Y%m%d"]:
                _ = self.format_birthday(birthday, type)
                if _ is not None:
                    birthday = _
                    flag = True
                    break
            if not flag:
                birthday = '0000-00-00'
        return birthday

    def format_birthday(self, birthday, type="%Y/%m/%d"):
        birthday = str(birthday) if isinstance(birthday, int) else birthday
        try:
            birthday = time.strptime(birthday, type)
            birthday = time.strftime("%Y-%m-%d", birthday)
        except:
            birthday = None
        return birthday

# 执行
def worker(task, msg, file_extension, work_table, line, index):
    try:
        p = Processor(task, msg, file_extension, work_table, line, index)
        p.run()
    except:
        log.error(traceback.format_exc())
    return

# 设置任务状态
def set_task_status(import_id, status) :
    sql = "UPDATE ml_import SET status='%d' WHERE id='%d'" % (int(status), import_id)
    res = mysql_pool.update(sql)
    return res

# 异常结束处理
def do_except(uid_tid_lid):
    (redis.pipeline()
     .lpush(EDM_WEB_MAIL_IMPORT_ERROR_QUEUE, uid_tid_lid)
     .hincrby(COMMON_VAR_COUNT_HASH,  'edm_web_mail_import_couont', -1)
     .execute())
    # redis.rpush(EDM_WEB_MAIL_IMPORT_ERROR_QUEUE, uid_tid_lid)
    # redis.hincrby(COMMON_VAR_COUNT_HASH, 'edm_web_mail_import_couont', -1)
    close_connect()
    sys.exit(1)

def do_text(task, filename, is_zip=True):
    if is_zip:
        log.info(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) start parsing.'.format(
            task['user_id'], task['list_id'], task['import_id'], pycharset.character_decode(filename, None, 'ignore'))
        )
    content = ''
    with open(filename, 'r') as f:
        # content = f.read()
        while 1:
            s = f.read()
            if not s: break
            content += s
    result = chardet.detect(content)
    confidence = result['confidence']
    charset = result['encoding']
    charset = charset.lower() if charset else None
    if not charset:
        if is_zip:
            log.error(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) charset can not be resolved!'.format(
                task['user_id'],task['list_id'],task['import_id'],pycharset.character_decode(filename, None, 'ignore')
            ))
        content = pycharset.character_decode(content, None, 'ignore')
        if not content:
            raise common.MyExceptionError(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) charset can not be resolved!'.format(
                task['user_id'],task['list_id'],task['import_id'],pycharset.character_decode(filename, None, 'ignore')
            ))
    else:
        if is_zip:
            log.info(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) charset={}, confidence={}'.format(
                task['user_id'], task['list_id'], task['import_id'], pycharset.character_decode(filename, None, 'ignore'), charset, confidence
            ))
        if charset == 'gb2312': charset = 'gb18030'
        content = pycharset.character_decode(content, charset, 'ignore')
    lines = content.replace('\r', '').split('\n')
    if task['is_ignore']:
        lines = lines[1:]
    if task['is_disorder']:
        random.shuffle(lines)
    return lines

def do_csv(task, filename, is_zip=True):
    if is_zip:
        log.info(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) start parsing.'.format(
            task['user_id'], task['list_id'], task['import_id'], filename
        ))
    with open(filename, 'r') as fp:
        lines = list(csv.reader(fp))
    if task['is_ignore']:
        lines = lines[1:]
    if task['is_disorder']:
        random.shuffle(lines)
    return lines

def do_excel(task, filename, is_zip=True):
    if is_zip:
        log.info(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) start parsing.'.format(
            task['user_id'], task['list_id'], task['import_id'], filename
        ))
    workbook = xlrd.open_workbook(filename)
    work_table = workbook.sheets()[0]
    lines = [i for i in xrange(work_table.nrows)]
    if task['is_ignore']:
        lines = lines[1:]
    if task['is_disorder']:
        random.shuffle(lines)
    return work_table, lines

def do_zip(task, filename):
    log.info(u'Import user_id:{}, list_id:{}, import_id:{}. file({}) start parsing.'.format(
        task['user_id'], task['list_id'], task['import_id'], filename
    ))
    path_to = os.path.join(ERR_ADDR_PATH, 'zip_{}_{}_{}'.format(task['user_id'], task['list_id'], task['import_id']))
    zfile.extract(filename, path_to)
    lines_list = []
    for parent, dirnames, filenames in os.walk(path_to):
        for _filename in filenames:
            _suffix = _filename.split('.')[-1]
            _suffix = _suffix.lower()
            _zfile = os.path.join(parent, _filename)
            if _suffix == 'txt':
                lines = time_call(do_text, task, _zfile, False)
                if lines is None:
                    log.error(u'Do_ZIP subset file is wrong!')
                    continue
                lines_count, _max_head = do_get_max_head(lines)
                if lines: lines_list.append([_suffix, None, lines, lines_count, _max_head])
            elif _suffix == 'csv':
                lines = time_call(do_csv, task, _zfile, False)
                if lines is None:
                    log.error(u'Do_ZIP subset file is wrong!')
                    continue
                lines_count, _max_head = do_get_max_head(lines)
                if lines: lines_list.append([_suffix, None, lines, lines_count, _max_head])
            elif _suffix in ['xls', 'xlsx']:
                res = time_call(do_excel, task, _zfile, False)
                if res is None:
                    log.error(u'Do_ZIP subset file is wrong!')
                    continue
                work_table, lines = res
                lines_count, _max_head = do_get_max_head(lines)
                if lines: lines_list.append([_suffix, work_table, lines, lines_count, _max_head])
    # 删除临时目录
    file_utils.remove_dir_file(path_to)
    log.info(u'Import user_id:{}, list_id:{}, import_id:{}. rm zipfile success.'.format( task['user_id'], task['list_id'], task['import_id'], filename))
    return lines_list

def do_get_max_head(lines):
    _max_head = 20
    lines_count = len(lines)
    if lines_count <= 10000:
        _max_head = 5
    elif lines_count <= 50000:
        _max_head = 8
    elif lines_count <= 100000:
        _max_head = 12
    return lines_count, _max_head

def scanner(msg, user_id, import_id, list_id):
    log.info(u'start {}'.format(msg))
    sql = "SELECT id, customer_id, maillist_id, filepath, is_disorder, is_ignore, status FROM ml_import WHERE id={} AND customer_id={} LIMIT 1".format(import_id, user_id)
    try:
        res = mysql_pool.getOne(sql)
    except:
        log.error(traceback.format_exc())
        close_file()
        do_except(uid_tid_lid)

    if not res:
        log.info(u'{} is None'.format(msg))
        return None

    task = {
        'import_id':    int(res[0]),
        'user_id':      int(res[1]),
        'list_id':      int(res[2]),
        'filepath':     str(res[3]),
        'is_disorder': int(res[4]),
        'is_ignore':    int(res[5]),
        'status':        str(res[6]),
    }
    if task['status'] != '0':
        return None

    if not os.path.exists(task['filepath']):
        set_task_status(task['import_id'], -2)
        log.info(u'{}. process error, not found import file.'.format(msg))
        return None

    file_extension = task['filepath'].split(".")[-1]
    file_extension = file_extension.lower()
    pool_limit = 20
    if file_extension == 'txt':
        lines = time_call(do_text, task, task['filepath'])
        if lines is None:
            log.error(u'{}. file({}) extension is wrong!'.format(msg, task['filepath']))
            set_task_status(task['import_id'], -2)
            return None
        lines_count, pool_limit = do_get_max_head(lines)
        lines_list=[[file_extension, None, lines, lines_count, pool_limit],]
    elif file_extension == 'csv':
        lines = time_call(do_csv, task, task['filepath'])
        if lines is None:
            log.error(u'{}. file({}) extension is wrong!'.format(msg, task['filepath']))
            set_task_status(task['import_id'], -2)
            return None
        lines_count, pool_limit = do_get_max_head(lines)
        lines_list=[[file_extension, None, lines, lines_count, pool_limit],]
    elif file_extension in ['xls', 'xlsx']:
        res = time_call(do_excel, task, task['filepath'])
        if res is None:
            log.error(u'{}. file({}) extension is wrong!'.format(msg, task['filepath']))
            set_task_status(task['import_id'], -2)
            return None
        work_table, lines = res
        lines_count, pool_limit = do_get_max_head(lines)
        lines_list=[[file_extension, work_table, lines, lines_count, pool_limit],]
    elif file_extension == 'zip':
        lines_list = time_call(do_zip, task, task['filepath'])
        if lines_list is None:
            log.error(u'{}. file({}) extension is wrong!'.format(msg, task['filepath']))
            set_task_status(task['import_id'], -2)
            return None
        elif lines_list is []:
            log.error(u'{}. file({}) is empty!'.format(msg, task['filepath']))
            set_task_status(task['import_id'], -2)
            return None
    else:
        return None

    import math
    pool = gevent.pool.Pool(pool_limit)
    for file_suffix, work_table, ilines, ilines_count, max_head in lines_list:
        avg_line = int(math.ceil(float(ilines_count)/float(max_head)))
        for index in xrange(max_head+1):
            if signal_stop: break
            start_index = avg_line*index
            end_index = avg_line*(index+1)
            line = ilines[start_index: end_index]
            if line:
                pool.spawn(worker, task, msg, file_suffix, work_table, line, index)
    pool.join()

    log.info(u'Import user_id:{}, list_id:{}, import_id:{}, status=1 (success)'.format( user_id, list_id, import_id))
    set_task_status(task['import_id'], 1)
    return task['filepath']

############################################################
# 安全调用对象
def safe_call(fn, *args, **kwargs):
    try :
        return fn(*args, **kwargs)
    except Exception, e:
        log.error('call "%s" failure\n %s' % (fn.__name__, e.message))
        log.error(traceback.format_exc())
        return None

# 等待调用成功 (有超时时间)
def time_call(fn, *args, **kwargs):
    try_count = 3
    while try_count > 0 :
        res = safe_call(fn, *args, **kwargs)
        if res is not None:
            return res
        log.error('try call "%s" count: %d' % (fn.__name__, try_count))
        try_count -= 1
        time.sleep(0.5)
    return

# 等待调用成功 (无超时时间)
def wait_call(fn, *args, **kwargs):
    while True :
        res = safe_call(fn, *args, **kwargs)
        if res is not None:
            return res
        time.sleep(0.5)
    return

############################################################
# 日志设置
def set_logger(log_file, is_screen=True):
    global log
    log = logging.getLogger('mail_import')
    log.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')

    log_handler = logging.handlers.RotatingFileHandler(log_file, 'a', 5000000, 4)
    log_handler.setFormatter(format)
    log.addHandler(log_handler)
    f = open(log_file, 'a')
    sys.stdout = f
    sys.stderr = f

    if is_screen:
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(format)
        log.addHandler(log_handler)

# 信号量处理
def signal_handle(mode):
    log.info(u"Catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

def init(msg, import_id, uid_tid_lid):
    global mysql_pool, mongo_cn, fp_err_t1, fp_err_t2
    conf = pyetc.load(os.path.join(ROOT, 'conf', 'setting.conf'))

    # 获取数据库
    dbconf = {'mysql': conf.mysql, 'mongo': conf.mongo}

    try:
        mysql_pool = MysqlPool.Mysql(dbconf, log)
    except BaseException as e:
        log.error(u'{}. init mysql pool exception.'.format(msg))
        log.error(traceback.format_exc())
        do_except(uid_tid_lid)

    try:
        mongo_cn = MongoPool.Mongo(dbconf, log)
        mongo_cn.init()
    except BaseException as e:
        log.error(traceback.format_exc())
        do_except(uid_tid_lid)

    try:
        # 错误类型 1
        err_t1_name = '{}_{}_err_t1.txt'.format(import_id, 'maillist')
        err_t1_path = os.path.join(ERR_ADDR_PATH, err_t1_name)
        fp_err_t1 = open(err_t1_path, "a")
        # 错误类型 2
        err_t2_name = '{}_{}_err_t2.txt'.format(import_id, 'maillist')
        err_t2_path = os.path.join(ERR_ADDR_PATH, err_t2_name)
        fp_err_t2 = open(err_t2_path, "a")
    except:
        log.error(u'{}. init error file failure.'.format(msg))
        do_except(uid_tid_lid)

def close_connect():
    mysql_pool.dispose()
    mongo_cn.dispose()
    return

def close_file():
    fp_err_t1.close()
    fp_err_t2.close()
    return

def finish(pid_file, filepath, operate, user_id, list_id, import_id):
    if operate == 'run':
        redis.hincrby(COMMON_VAR_COUNT_HASH, 'edm_web_mail_import_couont', -1)

    # 地址池 统计
    redis.rpush(EDM_WEB_USER_MAIL_IMPORT_COUNT_QUEUE, '{}_{}'.format(user_id, list_id))

    close_file()
    close_connect()

    if filepath and os.path.isfile(filepath):
        os.unlink(filepath)

    if os.path.exists(pid_file):
        os.unlink(pid_file)

if __name__ == "__main__":
    log_dir = os.path.join(ROOT, 'log')
    pid_dir = os.path.join(ROOT, 'pid')
    file_utils.make_dir([log_dir, pid_dir])
    log_file = os.path.join(log_dir, 'mail_import.log')
    # set_logger(log_file)
    set_logger(log_file, False)

    if len(sys.argv) <= 2:
        log.error("Command: {} uid_tid_listid <debug|run>\n".format(sys.argv[0]))
        sys.exit(1)

    uid_tid_lid = sys.argv[1]
    operate = sys.argv[2]
    user_id, import_id, list_id = uid_tid_lid.split('_')
    pid_file = os.path.join(pid_dir, 'mail_import_{}.pid'.format(import_id))
    pidfile.register_pidfile(pid_file)

    log.info(u'program start...')
    start_run_time = time.time()
    msg = u'Import user_id:{}, list_id:{}, import_id:{}'.format(user_id, list_id, import_id)
    init(msg, import_id, uid_tid_lid)
    EXIT_CODE = 0
    try:
        filepath = scanner(msg, user_id, import_id, list_id)
    except KeyboardInterrupt:
        signal_handle('sigint')
    except:
        log.error(traceback.format_exc())
        EXIT_CODE = 1

    finish(pid_file, filepath, operate, user_id, list_id, import_id)
    log.info(u"{}, spend total time: {}".format(msg, time.time()-start_run_time))
    log.info(u"program quit...")
    sys.exit(EXIT_CODE)
