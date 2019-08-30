# -*- coding: utf-8 -*-

import re
import StringIO
import email
import base64
import quopri
import email.utils
from email.header import decode_header
from email.generator import Generator
from email.parser import HeaderParser
from email._parseaddr import AddressList as _AddressList
try:
    import cchardet as chardet
except:
    import chardet

ecre = re.compile(r'''
  =\?                   # literal =?
  (?P<charset>[^?]*?)   # non-greedy up to the next ? is the charset
  \?                    # literal ?
  (?P<encoding>[qb])    # either a "q" or a "b", case insensitive
  \?                    # literal ?
  (?P<encoded>.*?)      # non-greedy up to the next ?= is the encoded string
  (?:\?=|$)
  ''', re.VERBOSE | re.IGNORECASE | re.MULTILINE)
email.header.ecre = ecre
email_compile = re.compile('^(\w|[-+=.])+@\w+([-.]\w+)*\.(\w+)$')


from logging import getLogger
# logger = getLogger("django.server")
logger = getLogger(__name__)
try:
    from app.utils.yctnefparse.tnef import TNEF
except:
    pass
try:
    from app.utils.string import decode_parse_content as _decode_content
except:
    def _decode_content(s=None, charset=None):
        """ 解析邮件
        """
        if not s:
            return s
        if charset:
            charset = charset.lower()
        if charset == 'utf-8':
            charset = 'utf-8'
        if charset in (
                'default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936', 'gb_1988-80', 'windows-1252', 'x-cp20936',
                "gb18030-2000"):
            # , 'hz-gb-2312'
            # 中文
            charset = 'gb18030'
        elif charset in (
                'chinese', 'csiso58gb231280', 'euc- cn', 'euccn', 'eucgb2312-cn', 'gb2312-1980', 'gb2312-80', 'iso- ir-58'):
            # 中文
            charset = 'gb2312'
        elif charset in ("936", "cp936", "ms936"):
            # 统一中文
            charset = 'gbk'
        elif charset in ("646", "us-ascii"):
            # 英文， ascii编码
            charset = 'ascii'
        elif charset in ("big5-tw", "csbig5"):
            # 繁体中文
            charset = 'big5'
        elif charset in ("big5-hkscs", "hkscs"):
            # 繁体中文
            charset = 'big5hkscs'
        elif charset in ("950", "ms950"):
            # 繁体中文
            charset = 'cp950'
        elif charset == "shift_jis":  # "euc-jp",
            # 日语
            charset = "iso-2022-jp"
        elif charset in ("ujis", "ujis", "u-jis"):
            # 日语
            charset = "euc-jp"
        elif charset in ("jisx0213", "eucjis2004"):
            # 日语
            charset = "euc_jis_2004"
        elif charset == "eucjisx0213":
            # 日语
            charset = "euc_jisx0213"
        elif charset in ("ks_c_5601-1987", "johab", "x-mac-korean", "x-cp20949"):
            # 韩语
            charset = "euc-kr"
        elif charset in ("euckr", "korean", "ksc5601", "ks_c-5601", "ks_c-5601-1987", "ksx1001", "ks_x-1001"):
            # 韩语
            charset = 'euc_kr'
        elif charset in ("ibm307", "ibm309"):
            # 英语
            charset = 'cp037'
        elif charset.startswith("windows-") or charset.startswith("windows_"):
            # windows
            charset = "cp" + charset[8:]
        elif charset.startswith("ibm"):
            # IBM
            charset = "cp" + charset[3:]
        elif charset in ("437", "ibm437"):
            # 英语
            charset = 'cp437'
        elif charset in ("ibm273", "csibm273", "273"):
            # 德语
            charset = 'cp273'
        elif charset in ("ibm424", "ebcdic-cp-he"):
            # 希伯来语
            charset = 'cp424'
        elif charset in ("ibm862", "862"):
            # 希伯来语
            charset = 'cp862'
        elif charset in ("ebcdic-cp-be", "ebcdic-cp-ch", "ibm500"):
            # 西欧
            charset = 'cp500'
        elif charset in ("850", "ibm850"):
            # 西欧
            charset = 'cp850'
        elif charset in ("858", "ibm858"):
            # 西欧
            charset = 'cp858'
        elif charset in ("852", "ibm852"):
            # 中欧和东欧
            charset = 'cp852'
        elif charset in ("855", "ibm855"):
            # 保加利亚语，白俄罗斯语，马其顿语，俄语，塞尔维亚语
            charset = 'cp855'
        elif charset in ("857", "ibm857"):
            # 土耳其
            charset = 'cp857'
        elif charset in ("860", "ibm860"):
            # 葡萄牙语
            charset = 'cp860'
        elif charset in ("861", "ibm861", "cp-is"):
            # 冰岛的
            charset = 'cp861'
        elif charset in ("ibm863", "863"):
            # 加拿大
            charset = 'cp863'
        elif charset in ("ibm865", "865"):
            # 丹麦语，挪威语
            charset = 'cp865'
        elif charset in ("ibm866", "866"):
            # 俄语
            charset = 'cp866'
        elif charset in ("ibm869", "869", "cp-gr"):
            # 希腊语
            charset = 'cp869'
        elif charset in ("932", "ms932", "mskanji", "ms-kanji"):
            # 日本
            charset = 'cp932'
        elif charset in ("949", "ms949", "uhc"):
            # 韩语
            charset = 'cp949'
        elif charset in ("1125", "ibm1125", "cp866u", "ruscii"):
            # 乌克兰
            charset = 'cp1125'

        # 解析
        is_charset_right, is_utf8_right, is_gbk_right = True, True, True
        try:
            s1 = s.decode(charset)
        except:
            is_charset_right = False

        # charset 可解析
        if is_charset_right:
            # if charset.startswith('utf') or charset.startswith("gb"):
            #     return s1
            if charset.startswith("iso-8859-") or charset.startswith("latin") or charset.startswith("iso8859_"):
                try:
                    return s.decode('gbk')
                except:
                    try:
                        return s.decode('gb18030')
                    except:
                        try:
                            return s.decode('utf-8')
                        except:
                            pass
            return s1
        else:
            try:
                # 若gb18030可以解析，直接返回
                return s.decode('gb18030')
            except:
                try:
                    # 若utf-8可以解析，直接返回
                    return s.decode('utf-8')
                except:
                    return s.decode(charset, 'ignore')
                    # try:
                    #     return s.decode(charset, 'ignore')
                    # except:
                    #     try:
                    #         return s.decode('utf-8', 'ignore')
                    #     except:
                    #         return s.decode('gb18030', 'ignore')


try:
    from .utils import email_parse_date
except:
    import datetime
    import traceback
    import dateutil.tz
    import dateutil.parser
    import calendar
    # import imaplib
    # from imapclient.fixed_offset import FixedOffset

    def decode_header_unicode_string(raw_string):
        """
        smtp获取邮件解析
        :param raw_string:
        :return: string(Unicode编码), charset(原始编码）
        """
        if not raw_string:
            return "", 'utf-8'
        raw_string = raw_string.replace('\n', '')

        # 对原始字符串进行兼容性处理，此处理只能针对 BASE64 编码，不能对 QUOTED-PRINTABLE
        # 编码进行操作
        if ('?B?' in raw_string or '?b?' in raw_string) and ('?==?' in raw_string):
            for _item in re.findall(r"(=\?.*?\?=)\S", raw_string):
                raw_string = raw_string.replace(_item, _item + ' ')

        # 对邮件主题进行初步解码
        try:
            parts = email.header.decode_header(raw_string)
        except Exception, err:
            logger.error("decode_header_unicode_string err: %s", (str(err),))
            return raw_string, 'utf-8'

        # 处理邮件主题
        full_str = ''
        charset = None
        for part in parts:
            # 判断当前部分的字符编码
            if part[1]:
                _charset = 'gbk' if part[1] == 'gb2312' else part[1]
                if part[1] == '136':
                    _charset = 'ascii'
            else:
                detectres = chardet.detect(part[0])
                if detectres["confidence"] >= 0.95:
                    _charset = detectres['encoding']
                else:
                    _charset = "gb18030"

            if _charset in (
                    'default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936', 'gb_1988-80', 'windows-1252'):
                # _charset = 'gbk'
                _charset = 'gb18030'
            _charset = _charset if _charset else 'gb18030'
            if charset is None:
                charset = _charset

            # 将当前部分追加至主题中
            part_str = _decode_content(part[0], _charset)
            # try:
            #     part_str = part[0].decode('gbk', 'ignore')
            # except UnicodeError, e:
            #     try:
            #         part_str = part[0].decode('utf-8', 'ignore')
            # except:
            #     part_str = part[0].decode('ascii', 'ignore')
            full_str += ' ' + part_str
        return full_str.lstrip(), charset

    # 解析时区信息
    def _parse_date_zone(raw_tz):
        zonem = int(raw_tz[3:]) + int(raw_tz[1:3]) * 60
        if raw_tz[0] == '-': zonem = -zonem
        return FixedOffset(zonem)

    def imap_parse_mail_date(raw_data=None):
        """ imap获取的邮件解析邮件时间
        """
        if raw_data is None:
            date_ = dateutil.parser.parse('1970-01-01 00:00:00 +0000')
            return date_.astimezone(dateutil.tz.tzlocal())
        #######################################################################
        raw_data = raw_data.replace('.', ':')
        # 2019.6.18 邮件时间问题，比如：Tue, 13 Oct 2009 12:30: 2 +0800，
        # # 2前面多了一个空格会解析错误，做了如下简单处理
        raw_data = raw_data.replace(': ', ':').replace(' :', ':')
        #######################################################################
        try:
            __, raw_data = raw_data.split(',')
        except:
            try:
                raw_data = decode_header_unicode_string(raw_data)[0]
                __, raw_data = raw_data.split(',')
            except:
                __, raw_data = raw_data.split(',')
        try:
            date_list = raw_data.split()
            if len(date_list) > 5:
                day, month, year, time_raw, tzinfo, _t = raw_data.split()
            else:
                day, month, year, time_raw, tzinfo = raw_data.split()
            hour, minute, second = time_raw.split(':')
            try:
                return datetime.datetime(
                    int(year), int(imaplib.Mon2num[month]), int(day),
                    int(hour), int(minute), int(second), 0,
                    _parse_date_zone(tzinfo))
            except:
                month = month.replace(u"月", "")
                return datetime.datetime(
                    int(year), int(month), int(day),
                    int(hour), int(minute), int(second), 0,
                    _parse_date_zone(tzinfo))
        except:
            try:
                raw_data = _decode_content(raw_data, charset="gb18030")
                date_list = raw_data.split()
                if len(date_list) > 5:
                    day, month, year, time_raw, tzinfo, _t = raw_data.split()
                else:
                    day, month, year, time_raw, tzinfo = raw_data.split()
                hour, minute, second = time_raw.split(':')
                month = (month.replace(u"十二月", "12").replace(u"十一月", "11").replace(u"十月", "10").replace(u"月", "")
                         .replace(u"九", "9").replace(u"八", "8").replace(u"七", "7").replace(u"六", "6").replace(u"五", "5")
                         .replace(u"四", "4").replace(u"三", "3").replace(u"二", "2").replace(u"一", "1")
                         )
                return datetime.datetime(
                    int(year), int(month), int(day),
                    int(hour), int(minute), int(second), 0,
                    _parse_date_zone(tzinfo))
            except:
                date_ = dateutil.parser.parse('1970-01-01 00:00:00 +0000')
                return date_.astimezone(dateutil.tz.tzlocal())

    def email_parse_date(msg_date):
        """ imap获取的邮件解析邮件收件人、发件人
        """
        return '1970-01-01 00:00:00 +0000'
        if not msg_date:
            date_ = dateutil.parser.parse('1970-01-01 00:00:00 +0000')
            return date_.astimezone(dateutil.tz.tzlocal())
        msg_date = msg_date.replace('.', ':')
        #######################################################################
        # 2019.6.18 邮件时间问题，比如：Tue, 13 Oct 2009 12:30: 2 +0800，
        # # 2前面多了一个空格会解析错误，做了如下简单处理
        msg_date = msg_date.replace(': ', ':').replace(' :', ':')
        date_ = email.utils.parsedate_tz(msg_date)
        #######################################################################

        if date_ and not date_[9] is None:
            ts = email.utils.mktime_tz(date_)
            date_ = datetime.datetime.utcfromtimestamp(ts)
        else:
            date_ = email.utils.parsedate(msg_date)
            if date_:
                ts = calendar.timegm(date_)
                date_ = datetime.datetime.utcfromtimestamp(ts)
            else:
                return imap_parse_mail_date(msg_date)
        if date_.tzname() is None:
            date_ = date_.replace(tzinfo=dateutil.tz.tzutc())
        return date_.astimezone(dateutil.tz.tzlocal())

def amend_getaddresses(raw_value):
    """Return a list of (REALNAME, EMAIL) for each fieldvalue.
    """
    if not raw_value:
        return []
    addresslist = email.utils.getaddresses(raw_value)
    lst = []
    error = []
    for i in addresslist:
        if email_compile.search(i[1]):
            error.append(i[0])
            lst.append( (" ".join(error), i[1]) )
            error = []
        else:
            error.append(i[1])
    return lst

def amend_parseaddr(raw_value):
    """Return a list of (REALNAME, EMAIL) for each fieldvalue.
    """
    # addrs = email.utils.parseaddr(raw_value)
    addrs = _AddressList(raw_value).addresslist
    if not addrs:
        return '', ''
    lst = []
    error = []
    for i in addrs:
        if email_compile.search(i[1]):
            error.append(i[0])
            lst.append((" ".join(error), i[1]))
            break
        else:
            error.append(i[1])
    return lst[0]


class MailParser(object):
    invalid_chars_in_filename = '<>:"/\\|?*\%\'' + \
                                reduce(lambda x, y: x + chr(y), range(32), '')
    invalid_windows_name = 'CON PRN AUX NUL COM1 COM2 COM3 COM4 COM5 COM6 COM7 COM8 COM9 LPT1 LPT2 LPT3 LPT4 LPT5 LPT6 LPT7 LPT8 LPT9'.split()

    atom_rfc2822 = r"[a-zA-Z0-9_!#\$\%&'*+/=?\^`{}~|\-]+"

    # without '!' and '%'
    atom_posfix_restricted = r"[a-zA-Z0-9_#\$&'*+/=?\^`{}~|\-]+"

    atom = atom_rfc2822

    dot_atom = atom + r"(?:\." + atom + ")*"

    quoted = r'"(?:\\[^\r\n]|[^\\"])*"'

    local = "(?:" + dot_atom + "|" + quoted + ")"

    domain_lit = r"\[(?:\\\S|[\x21-\x5a\x5e-\x7e])*\]"

    domain = "(?:" + dot_atom + "|" + domain_lit + ")"

    addr_spec = local + "\@" + domain

    email_address_re = re.compile('^' + addr_spec + '$')

    headers = dict()

    def __init__(self, mail_orig, contain_data=False, fmore=False, transe_winmaildat=False):
        self.mail_orig = mail_orig
        self.plain_text = ''
        self.html_text = ''
        self.plain_charset = ''
        self.html_charset = ''
        self.obj = email.message_from_string(self.mail_orig)
        self.charset = ''
        self.sid = 0
        # 获取附件内容
        # self.contain_data = contain_data
        self.contain_data = True
        # 获取更多其他信息
        self.fmore = fmore
        # 转换winmail.dat
        # self.transe_winmaildat = transe_winmaildat
        self.transe_winmaildat = True
        self.attachments = []

    # 解析邮件模板
    def parseMailTemplate(self, is_walk=True, is_walk_html=False):
        message = {}
        try:
            msg = self.obj
            message['subject'] = self.get_attr('subject')
            message['mfrom'] = self.get_attr('from')
            message['to'] = self.get_attr('to')
            message['cc'] = self.get_attr('cc')
            message['bcc'] = self.get_attr('bcc')
            message['date'] = self.get_attr('date')
            message['message_id'] = self.get_attr('message-id')
            message['reply_to'] = self.get_attr('reply-to')
            message['sender'] = self.get_attr('sender')
            message['plain_text'] = self.plain_text
            message['html_text'] = self.html_text
            message['plain_charset'] = self.plain_charset
            message['html_charset'] = self.html_charset
            message['mail_level'] = self.get_attr('X-MailSecurity')
            if self.fmore:
                message['X-MailPassword'] = self.get_attr('x-mailpassword')
                message['X-MailBurn'] = self.get_attr('X-mailburn')
                # maila['X-MailBurnLimit'] = self.get_attr('X-MailBurnLimit')
                # maila['X-MailBurnDay'] = self.get_attr('X-MailBurnDay')
                message['X-MailSchedule'] = self.get_attr('x-mailschedule')
                message['X-MailScheduleDay'] = self.get_attr('x-mailscheduleDay')
                message['Disposition-Notification-To'] = self.get_attr('disposition-notification-to')
                message['X-MailCalendar'] = self.get_attr('x-mailcalendar')
                message['X-MailCalendarEvent'] = self.get_attr('x-mailcalendarevent')
                message['X-MailCalendarEventID'] = self.get_attr('x-mailcalendareventid')
                message['Return-Path'] = self.get_attr('return-path')

            attachments = self.get_mail_contents(msg)
            self.attachments = attachments
            message['plain_text'] = self.plain_text
            message['html_text'] = self.html_text
            message['plain_charset'] = self.plain_charset
            message['html_charset'] = self.html_charset
            message['attachments'] = attachments
        except Exception as e:
            logger.error(traceback.format_exc())
            raise Exception(e)
        return message

    # 取得指定头解码后的内容
    def get_attr(self, field, default=None):
        field = field.lower()
        if field == 'subject':  # subject
            raw_value = self.obj.get(field, None)
            if raw_value is None: return default
            return self.decode_header_string(raw_value)[0]
        elif field == 'from':  # from
            raw_value = self.obj.get(field, None)
            if raw_value is None: return default
            try:
                # 处理地址
                addresses = list(amend_parseaddr(raw_value))
                return addresses[1], self.decode_header_string(addresses[0])[0]
            except BaseException as e:
                try:
                    return self.decode_header_string(raw_value)[0], ''
                except:
                    return raw_value, ''
        elif field in ('sender', 'disposition-notification-to', 'reply-to'):
            # 取得原始字符串
            raw_value = self.obj.get(field, None)
            if raw_value is None: return default
            try:
                # 处理地址
                addresses = list(amend_parseaddr(raw_value))
                return addresses[1]
            except BaseException as e:
                try:
                    return self.decode_header_string(raw_value)[0]
                except:
                    return raw_value
        elif field in ('to', 'cc', 'bcc'):  # to, cc
            # 取得原始数据列表
            raw_value = self.obj.get_all(field, None)
            if raw_value is None: return default
            # 处理地址列表
            try:
                raw_list = amend_getaddresses(raw_value)
                if not raw_list:
                    return []
                new_list = []
                for addresses in raw_list:
                    addresses = list(addresses)
                    new_list.append([addresses[1], self.decode_header_string(addresses[0])[0]])
                if new_list:
                    return new_list
                else:
                    try:
                        new_list = []
                        for _raw_value in raw_value:
                            _ls = self.decode_header_string(_raw_value)[0]
                            if not _ls: continue
                            new_list.append([_ls, ''])
                        return new_list
                    except:
                        return [(i, '') for i in raw_value]
            except BaseException as e:
                try:
                    new_list = []
                    for _raw_value in raw_value:
                        new_list.append([self.decode_header_string(_raw_value)[0], ''])
                    return new_list
                except:
                    return [(i, '') for i in raw_value]
        elif field == 'date':  # date
            return self._get_date()
        elif field == 'message-id':
            raw_value = self.obj.get(field, default)
            return raw_value
        return self.obj.get(field, default)


    def get_mail_contents(self, msg):
        """split an email in a list of attachments"""

        attachments = []

        # retrieve messages of the email
        # bodies = self.search_message_bodies(msg)

        # reverse bodies dict
        # parts = dict((v,k) for k, v in bodies.iteritems())

        # organize the stack to handle deep first search
        stack=[ msg, ]
        while stack:
            part = stack.pop(0)
            content_type = part.get_content_type()
            is_multipart = part.is_multipart()
            if content_type.startswith('message/'):
                attachment = self._get_attachment(
                    part, is_multipart, contain_data=self.contain_data, transe_winmaildat=self.transe_winmaildat)
                if attachment:
                    if isinstance(attachment, list):
                        attachments.extend(attachment)
                    else:
                        # elif attachment['type'] == 'attachment':
                        attachments.append(attachment)
            elif part.is_multipart():
                # insert new parts at the beginning
                # of the stack (deep first search)
                stack[:0]=part.get_payload()
            else:
                if self.is_attachment(part):
                    attachment = self._get_attachment(
                        part, is_multipart, contain_data=self.contain_data, transe_winmaildat=self.transe_winmaildat)
                    if attachment:
                        if isinstance(attachment, list):
                            attachments.extend(attachment)
                        else:
                            attachments.append(attachment)
                elif not is_multipart and part.get_content_subtype() in ['html', 'plain']:
                    self._parse_text(part)
        return attachments

    def search_message_bodies(self, mail):
        """search message content into a mail"""
        bodies = dict()
        self._search_message_bodies(bodies, mail)
        return bodies

    def _search_message_bodies(self, bodies, part):
        """recursive search of the multiple version of the 'message' inside
        the the message structure of the email, used by search_message_bodies()
        """

        type = part.get_content_type()
        if type.startswith('multipart/'):
            # explore only True 'multipart/*'
            # because 'messages/rfc822' are also python 'multipart'
            if type == 'multipart/related':
                # the first part or the one pointed by start
                start = part.get_param('start', None)
                related_type = part.get_param('type', None)
                for i, subpart in enumerate(part.get_payload()):
                    if (not start and i==0) or \
                            (start and start==subpart.get('Content-Id')):
                        self._search_message_bodies(bodies, subpart)
                        return
            elif type=='multipart/alternative':
                # all parts are candidates and latest is best
                for subpart in part.get_payload():
                    self._search_message_bodies(bodies, subpart)
            elif type in ('multipart/report',  'multipart/signed'):
                # only the first part is candidate
                try:
                    subpart=part.get_payload()[0]
                except IndexError:
                    return
                else:
                    self._search_message_bodies(bodies, subpart)
                    return

            elif type=='multipart/signed':
                # cannot handle this
                return

            else:
                # unknown types must be handled as 'multipart/mixed'
                # This is the peace of code could probably be improved,
                # I use a heuristic :
                # - if not already found,
                #      use first valid non 'attachment' parts found
                for subpart in part.get_payload():
                    tmp_bodies=dict()
                    self._search_message_bodies(tmp_bodies, subpart)
                    for k, v in tmp_bodies.iteritems():
                        if not subpart.get_param('attachment',
                                                 None, 'content-disposition')=='':
                            # if not an attachment, initiate value
                            # if not already found
                            bodies.setdefault(k, v)
                return
        else:
            bodies[part.get_content_type().lower()]=part
            return
        return

    def get_or_set_charset(self):
        """
        获取当前邮件的默认编码,
        如果没有, 则根据邮件主题的编码判断
        :param charset:
        :return:
        """

        if not self.charset:
            s, code = decode_header(self.compatible_string(self.obj.get('Subject', '')))[0]
            self.charset = self.guess_charset(s, code)
        return self.charset

    def guess_charset(self, str, code):
        """
        判断邮件编码
        s, code = decode_header(self.obj.get('subject'))[0]
        :param str:
        :param code:
        :return:
        """
        if code:
            code = code.lower()
            _charset = 'gbk' if code == 'gb2312' else code
            if code == '136': _charset = 'ascii'
        else:
            detectres = chardet.detect(str)
            if detectres["confidence"] >=0.95:
                _charset = detectres['encoding']
            else:
                _charset = "gb18030"
        # if _charset in ['default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936']:
        if _charset in ('default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936', 'gb_1988-80', 'windows-1252'):
            _charset = 'gb18030'
        return _charset if _charset else 'gb18030'

    def compatible_string(self, raw_string):
        # 对原始字符串进行兼容性处理，此处理只能针对 BASE64 编码，不能对 QUOTED-PRINTABLE
        # 编码进行操作
        raw_string = raw_string.replace('\n', '')
        if ('?B?' in raw_string or '?b?' in raw_string) and ('?==?' in raw_string):
            for _item in re.findall(r"(=\?.*?\?=)\S", raw_string):
                raw_string = raw_string.replace(_item, _item + ' ')
        return raw_string

    def decode_header_string(self, raw_string, to_charset=''):
        """
        对邮件内容进行解码
        :param raw_string: 原邮件内容
        :param to_charset: 需要解码成的字符类型, 默认空, 表示unicode
        :return:
        """
        if raw_string is None: return "", to_charset
        raw_string = self.compatible_string(raw_string)

        try:
            parts = email.header.decode_header(raw_string)
        except:
            return raw_string, to_charset

        full_str = ''
        for part in parts:
            _charset = self.guess_charset(part[0], part[1])
            part_str = _decode_content(part[0], _charset)
            full_str += u' ' + part_str
        if to_charset:
            return full_str.lstrip().encode(to_charset, 'ignore'), to_charset
        else:
            return full_str.lstrip(), ''

    # 解析时间
    def _get_date(self):
        return email_parse_date(self.obj.get('date', ''))

    def get_filename(self, part):
        """Many mail user agents send attachments with the filename in
        the 'name' parameter of the 'content-type' header instead
        of in the 'filename' parameter of the 'content-disposition' header.
        """
        filename=part.get_param('filename', None, 'content-disposition')
        if not filename:
            filename=part.get_param('name', None) # default is 'content-type'
        if not filename:
            filename=part.get_param('alt', None)

        if filename:
            # RFC 2231 must be used to encode parameters inside MIME header
            filename=email.Utils.collapse_rfc2231_value(filename).strip()

        if filename and isinstance(filename, str):
            # But a lot of MUA erroneously use RFC 2047 instead of RFC 2231
            # in fact anybody miss use RFC2047 here !!!
            filename = decode_header(filename)
        return filename

    def decode_text(self, payload, charset=None):
        return _decode_content(payload, charset), charset

    def _parse_text(self, part):
        subtype = part.get_content_subtype()
        #######################################################################################
        # 简单暴力处理问题邮件的问题，  2019.5.20
        # [('Content-Type', 'text/html; charset="gb18030"'), ('MIME-Version', '1.0'), ('Content-Transfer-Encoding', 'base64')]
        if ( not part.get('Content-Transfer-Encoding', None) and not part.get('Content-Type', None)):
            return
        #######################################################################################

        #############################
        # 剔除不是邮件内容的部分
        if part.get_content_maintype() != 'text':
            return

        text = part.get_payload()
        if not text:
            return ''
        charset = part.get_param('charset', '').lower()
        if not charset:
            charset = self.get_or_set_charset()
            if charset:
                charset = charset.lower()

        if charset in ['default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936']:
            charset = 'gb18030'
            # charset = 'gbk'

        body_code = part.get('Content-Transfer-Encoding', '').lower()
        try:
            if body_code == 'base64':
                text = base64.decodestring(text)
            elif body_code == 'quoted-printable':
                text = quopri.decodestring(text)
            else:
                text = text
        except BaseException, e:
            text = text

        if subtype == 'html':
            self.html_text = _decode_content(text, charset)
        elif subtype == 'plain':
            self.plain_text = _decode_content(text, charset)

    def _get_attachment(self, part, is_multipart=False, contain_data=True, transe_winmaildat=False):
        content_disposition = part.get('Content-Disposition', '')
        _mail_level = part.get('X-MailSecurity', '')
        attachment = {}
        self.sid += 1
        filename = part.get_filename()
        attachment['sid'] = self.sid
        attachment['did'] = ''
        attachment['name'] = self.decode_header_string(filename)[0]
        attachment['mail_level'] = _mail_level
        if is_multipart:
            content_type = part.get_content_type()
            # data = part.as_string()

            content_transfer_encoding = part.get('Content-Transfer-Encoding', '')
            parts = part.get_payload()
            data = ""
            data2 = ""
            for n, part2 in enumerate(parts):
                try:
                    message = part2.as_string()
                    if content_transfer_encoding == "base64":
                        data2 = base64.decodestring(message)
                    elif content_transfer_encoding == "quoted-printable":
                        data2 = quopri.decodestring(message)
                    else:
                        data2 = message
                except:
                    if content_type.startswith('message/'):
                        fp = StringIO.StringIO()
                        g = Generator(fp, mangle_from_=False)
                        g.flatten(part, unixfrom=False)
                        data2 = fp.getvalue()
                    else:
                        data2 = message
                if data2:
                    data += data2
            if not data:
                data = part.as_string()

            if not attachment['name']:
                if content_type.startswith("message/delivery-status"):
                    attachment['name'] = "details.txt"
                elif content_type.startswith("message/rfc822"):
                    try:
                        parser = HeaderParser()
                        _headers = parser.parsestr(data)
                        _Subject = self.decode_header_string(_headers.get("Subject"))[0]
                        attachment['name'] = u"{}.eml".format(
                            _Subject.replace("/", "_").replace("\\", "_") if _Subject else "mail"
                        )
                    except:
                        print
                        attachment['name'] = "mail.eml"
                else:
                    attachment['name'] = "Unkown"

        else:
            data = part.get_payload(decode=True)
        if contain_data:
            attachment['data'] = data
        attachment['size'] = len(data)
        for k in part.keys():
            attachment[k.lower().replace('-', '_')] = part.get(k)
        if 'content_id' in attachment:
            attachment['content_id'] = attachment.get('content_id')[1:-1]
        else:
            attachment['content_id'] = ''

        if content_disposition.startswith('attachment'):
            attachment['type'] = 'attachment'
        elif not attachment['content_id']:
            attachment['type'] = 'attachment'
        else:
            attachment['type'] = 'inline'

        if 'content_type' in attachment:
            attachment['content_type'] = attachment['content_type'].split(';')[0]
        else:
            attachment['content_type'] = 'application/octet-stream'

        # winmail.dat 邮件附件解析
        if transe_winmaildat and attachment["name"] == u'winmail.dat' and attachment['type'] == 'attachment' and \
                attachment['content_type'] == "application/ms-tnef":
            try:
                t = TNEF(data, do_checksum=True)
                did = 1
                _attachment1 = []
                for a in t.attachments:
                    _data = a.data
                    _name = a.long_filename()
                    _attachment2 = {
                        # 'content_disposition': u'attachment;\r\n\tfilename="{}"'.format(_name),
                        'content_id': attachment['content_id'],
                        'content_transfer_encoding': 'base64',
                        'content_type': 'application/octet-stream',
                        'name': a.long_filename(),
                        'sid': attachment['sid'],
                        'size': len(_data),
                        'type': 'attachment',
                        'did': did,
                        'mail_level': attachment['mail_level'],
                    }
                    did += 1
                    if contain_data:
                        _attachment2['data'] = _data
                    _attachment1.append(_attachment2)
                return _attachment1
            except:
                if "content_disposition" in attachment:
                    del attachment["content_disposition"]
                return attachment
        if "content_disposition" in attachment:
            del attachment["content_disposition"]
        return attachment

    def is_attachment(self, part):
        if (
                part.get('Content-Disposition', '').startswith('attachment') or
                self.get_filename(part) or
                part.get('Content-ID', '') or
                (part.get('Content-Type', '') and part.get('Content-Type', '').startswith("message/"))
        ):
            return True
        return False

    def has_attachment(self):
        """ 上传邮件使用，打标记umail-attach
        邮件包含附件
        """
        if self.attachments:
            for i in self.attachments:
                if i['type'] == "attachment":
                    return True
            return True
        # retrieve messages of the email
        # bodies = self.search_message_bodies(self.obj)
        # reverse bodies dict
        # parts = dict((v, k) for k, v in bodies.iteritems())
        # organize the stack to handle deep first search
        stack = [self.obj, ]
        while stack:
            part = stack.pop(0)
            content_type = part.get_content_type()
            is_multipart = part.is_multipart()
            if content_type.startswith('message/'):
                attachment = self._get_attachment(
                    part, is_multipart, contain_data=self.contain_data, transe_winmaildat=self.transe_winmaildat)
                if isinstance(attachment, list):
                    return True
                else:
                    if attachment['type'] == "attachment":
                        return True
            elif part.is_multipart():
                # insert new parts at the beginning
                # of the stack (deep first search)
                stack[:0] = part.get_payload()
            else:
                if self.is_attachment(part):
                    attachment = self._get_attachment(
                        part, is_multipart, contain_data=self.contain_data, transe_winmaildat=self.transe_winmaildat)
                    if isinstance(attachment, list):
                        return True
                    else:
                        if attachment['type'] == "attachment":
                            return True
        return False

    def get_attachment(self, sid=None, cid=None, did=None, contain_data=False):
        contain_data = True
        if self.attachments:
            for _attachment in self.attachments:
                if did and sid and str(_attachment.get('did', '')) == did and str(_attachment.get('sid', '')) == sid:
                    return _attachment
                elif cid and _attachment.get('content_id', '') == cid:
                    return _attachment
                elif sid and str(_attachment.get('sid', '')) == sid:
                    return _attachment
            return {}

        # retrieve messages of the email
        # bodies = self.search_message_bodies(self.obj)
        # reverse bodies dict
        # parts = dict((v, k) for k, v in bodies.iteritems())
        # organize the stack to handle deep first search
        stack = [self.obj, ]
        while stack:
            part = stack.pop(0)
            content_type = part.get_content_type()
            is_multipart = part.is_multipart()
            if content_type.startswith('message/'):
                attachment = self._get_attachment(
                    part, is_multipart, contain_data=contain_data, transe_winmaildat=True)
                if attachment:
                    if isinstance(attachment, list):
                        for _attachment in attachment:
                            if str(_attachment.get('did', '')) == did and str(_attachment.get('sid', '')) == sid:
                                return _attachment
                    else:
                        if cid and attachment.get('content_id', '') == cid:
                            return attachment
                        elif sid and str(attachment.get('sid', '')) == sid:
                            return attachment
            elif part.is_multipart():
                # insert new parts at the beginning
                # of the stack (deep first search)
                stack[:0] = part.get_payload()
            else:
                if self.is_attachment(part):
                    attachment = self._get_attachment(
                        part, is_multipart, contain_data=contain_data, transe_winmaildat=True)
                    if attachment:
                        if isinstance(attachment, list):
                            for _attachment in attachment:
                                if str(_attachment.get('did', '')) == did and str(_attachment.get('sid', '')) == sid:
                                    return _attachment
                        else:
                            if cid and attachment.get('content_id', '') == cid:
                                return attachment
                            elif sid and str(attachment.get('sid', '')) == sid:
                                return attachment
        return {}


if __name__ == "__main__":
    import pprint
    path = "../bug1.eml"
    # path = "bug1.eml"
    # path = "xxxxxxxxxxxxxxxxxx.eml"
    # path = u"0000.eml"
    raw = open(path).read()
    parse = MailParser(raw, False)
    message = parse.parseMailTemplate()
    pprint.pprint(message)
    # print len( message["attachments"])

    # html_text = message['html_text']
    # RE_CID = re.compile("""["|']cid:(?P<cid>[^"']+)""")
    # print html_text
    # for cid in RE_CID.findall(html_text):
    #     print cid
    #     IMGdata = parse.get_attachment(cid=cid, contain_data=True).get('data', '')
    #     print len(IMGdata)