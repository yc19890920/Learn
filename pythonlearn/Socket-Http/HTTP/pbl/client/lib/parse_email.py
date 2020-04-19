# coding=utf-8
"""
解析邮件
"""
import re

import copy
import email
import base64
import quopri
import datetime
import calendar
from email.header import decode_header
import email.utils

import dateutil.tz
import dateutil.parser
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

class ParseEmail():
    def __init__(self, mail_orig):
        # self.mail_orig = mail_orig.encode('ascii', 'ignore')
        self.mail_orig = mail_orig
        self.plain_text = ''
        self.html_text = ''
        self.plain_charset = ''
        self.html_charset = ''
        self.obj = email.message_from_string(self.mail_orig)
        self.charset = ''

    # 解析邮件模板
    def parseMailTemplate(self):

        maila = {}
        attachments = []
        for part in self.obj.walk():
            if part.is_multipart(): continue
            attachment = self._get_attachment(part)
            if attachment:
                attachments.append(attachment)
            self._parse_text(part)

        maila['subject'] = self.get_attr('subject')
        maila['from'] = self.get_attr('from')
        maila['to'] = self.get_attr('to')
        maila['date'] = self.get_attr('date')
        maila['plain_text'] = self.plain_text
        maila['html_text'] = self.html_text
        maila['plain_charset'] = self.plain_charset
        maila['html_charset'] = self.html_charset
        maila['attachments'] = attachments
        return maila

    def _parse_text(self, part):
        # 剔除不是邮件内容的部分
        if part.get_content_maintype() != 'text':
            return

        text = part.get_payload()
        if not text:
            return ''
        charset = part.get_param('charset', '').lower()
        if not charset:
            charset = self.get_or_set_charset()


        if charset in ['default', 'us-ascii', 'gb2312', 'iso-2022-cn', 'windows-936']:
            charset = 'gbk'

        # 解码内容
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


        # 根据type类型 设置text值
        subtype = part.get_content_subtype()
        if subtype == 'html':
            self.html_text = text
            self.html_charset = charset
        else:
            self.plain_text = text
            self.plain_charset = charset
        return

    def _get_date(self):
        msg_date = self.obj.get('date', '').replace('.', ':')
        if not msg_date:
            return ''
        date_ = email.utils.parsedate_tz(msg_date)

        if date_ and not date_[9] is None:
            ts = email.utils.mktime_tz(date_)
            date_ = datetime.datetime.utcfromtimestamp(ts)
        else:
            date_ = email.utils.parsedate(msg_date)
            if date_:
                ts = calendar.timegm(date_)
                date_ = datetime.datetime.utcfromtimestamp(ts)
            else:
                date_ = dateutil.parser.parse('1970-01-01 00:00:00 +0000')

        if date_.tzname() is None:
            date_ = date_.replace(tzinfo=dateutil.tz.tzutc())
        return date_

    def _get_attachment(self, part):
        if part.get('Content-Disposition', '').startswith('attachment') or part.get_param('name'):
            attachment = {}
            filename = part.get_filename()
            attachment['name'] = filename
            attachment['decode_name'] = self.decode_header_string(filename)[0]
            data = part.get_payload(decode=True)
            attachment['data'] = data
            attachment['size'] = len(data)
            for k in part.keys():
                attachment[k.lower().replace('-', '_')] = part.get(k)
            if 'content_id' in attachment:
                attachment['content_id'] = attachment.get('content_id')[1:-1]
            return attachment
        return None

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
            _charset = chardet.detect(str)['encoding']
        return _charset if _charset else 'gbk'


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

        # 对邮件主题进行初步解码
        try:
            parts = email.header.decode_header(raw_string)
        except:
            return raw_string, to_charset

        # 处理邮件主题
        full_str = ''
        for part in parts:
            # 判断当前部分的字符编码
            _charset = self.guess_charset(part[0], part[1])
            try:
                part_str = part[0].decode(_charset, 'ignore')
            except BaseException, e:
                try:
                    part_str = part[0].decode('utf-8', 'ignore')
                except BaseException, e:
                    part_str = part[0]

            full_str += u' ' + part_str
        if to_charset:
            return full_str.lstrip().encode(to_charset, 'ignore'), to_charset
        else:
            return full_str.lstrip(), ''


    # 取得指定头解码后的内容
    def get_attr(self, field, default=None):

        field = field.lower()

        # subject
        if field in ['subject']:
            raw_value = self.obj.get(field, None)
            if raw_value is None: return default
            return self.decode_header_string(raw_value)[0]

        # from, sender
        elif field in ['from', 'sender']:

            # 取得原始字符串
            raw_value = self.obj.get(field, None)
            if raw_value is None: return default

            try:
                # 处理地址
                addresses = list(email.utils.parseaddr(raw_value))
                addresses[0] = self.decode_header_string(addresses[0])[0]
                try:
                    addresses[1] = u'(%s)' % addresses[1]
                except UnicodeError:
                    addresses[1] = '(XXXX)'
                return addresses[1] if addresses[0] == '' else ' '.join(addresses)
            except BaseException as e:
                print e
                return raw_value


        # to, cc
        elif field in ['to', 'cc', 'bcc']:

            # 取得原始数据列表
            raw_value = self.obj.get_all(field, None)
            if raw_value is None: return default

            # 处理地址列表
            try:
                raw_list = email.utils.getaddresses(raw_value)
                new_list = []
                for addresses in raw_list:
                    addresses = list(addresses)
                    addresses[0] = self.decode_header_string(addresses[0])[0]
                    try:
                        addresses[1] = '(%s)' % addresses[1]
                    except UnicodeError:
                        addresses[1] = '(XXXX)'
                    new_list.append(addresses[1] if addresses[0] == '' else ' '.join(addresses))
                return ', '.join(new_list)
            except BaseException as e:
                return raw_value

        # date
        elif field == 'date':
            return self._get_date()
        # 其它
        return self.obj.get(field, default)


    def get_simple_attr(self, attr):
        return email.utils.parseaddr(self.obj.get(attr, ''))[1].lower()

    # 获取邮件模板内容, html或plain, 优先html内容
    def get_content(self, data=None):
        if not data:
            data = self.parseMailTemplate()
        content = data['html_text']
        charset = data['html_charset']
        if not content:
            content = data['plain_text']
            charset = data['plain_charset']
        try:
            content = content.decode(charset, 'ignore')
        except BaseException as e:
            try:
                content = content.decode('gbk', 'ignore')
            except BaseException as e:
                content = content.decode('utf-8', 'ignore')
        return content

    def get_login_username(self):
        try:
            return re.search('\(Authenticated sender: (.*?)\)', self.obj.get('Received')).group(1).strip()
        except:
            return ''

if __name__ == "__main__":
    # email_str = open("/home/comingchina/work/mail-relay/web/lib/c.eml", "r").read()
    # email_str = open('/home/comingchina/documents/eml(8).eml').read()
    email_str = open(r'D:\code\POP3\pop3mail_10120388.eml').read()
    p = ParseEmail(email_str)
    # print p.get_login_username()
    # data = p.parseMailTemplate()
    # attaches = data.get('attachments', [])
    # content = p.get_content(data)
    # with open('/tmp/tmp.tpl', 'w') as fw:
    #     fw.write(content.encode('utf-8'))

    # for a in attaches:
    #     print a['name']
    # print p.get_attr()
    print p.get_simple_attr('from')
    print p.get_attr('from')
    s = p.get_attr('X-EsetResult')
    s = p.get_attr('X-ESET-Antispam', '')
    print type(s)
    print s


    # print get_mail_subject(mail_data=email_str)
    # print
    rs = p.parseMailTemplate()
    import pprint
    pprint.pprint(rs)