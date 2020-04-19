# -*- coding: utf-8 -*-
#

import time, email, base64, quopri, uuid


from email.header import decode_header, make_header

class ReplaceEmail(object):


    def __init__(self, msg):
        self.mail_orig = msg
        # 设置发送日期
        self.mail_date = time.strftime("%a, %d %b %Y %H:%M:%S %z")

        # 解析邮件模板
        self.__parseMailTemplate()

    def __parseMailTemplate(self):
        obj = email.message_from_string(self.mail_orig)

        # 解析邮件主题
        tmp = decode_header(obj.get('Subject'))[0]
        self.__setMailCharset(tmp[1])
        self.mail_subj = self.__convertCharset(tmp[0], self.charset)

        # 解析邮件主题列表 add 2016.10.26
        # subject_tmp = []
        # for each in self.subject_list:
        #     try:
        #         s = self._encode_str(each)
        #     except:
        #         s = self._decode_str(each)
        #     subject_tmp.append(s)
        # self.subject_list = subject_tmp

        # 分解邮件内容
        part = None
        for part in obj.walk():
            # 剔除不是邮件内容的部分
            if part.is_multipart(): continue
            if part.get_content_maintype() != 'text': continue

            # 取出邮件内容，html 格式优先
            subtype = part.get_content_subtype()
            self.body_orig = part.get_payload()
            if subtype == 'html': break

        # 解码内容
        self.body_code = part.get('Content-Transfer-Encoding')
        if self.body_code == 'base64':
            self.body_text = base64.decodestring(self.body_orig)
        elif self.body_code == 'quoted-printable':
            self.body_text = quopri.decodestring(self.body_orig)
        else:
            self.body_text = self.body_orig
        self.body_text = self.__convertCharset(self.body_text, self.charset)

        return

    # 设置当前邮件的字符编码
    def __setMailCharset(self, charset):
        if not charset:
            charset = 'utf-8'
        else:
            charset = charset.lower()
            if charset == 'gb2312': charset = 'gbk'
        self.charset = charset

    def __convertCharset(self, string, from_charset, to_charset='utf-8'):
        if from_charset.lower() == to_charset.lower(): return string
        s = string.decode(from_charset)
        s = s.encode(to_charset)
        return s

    # 生成编码后的邮件地址
    def __makeEncodeAddr(self, address, name=None):
        if name:
            name = name.decode('utf-8')
            en_name = str(make_header([(name, self.charset)]))
        else:
            en_name = None
        address = email.utils.formataddr((en_name, address))
        return address

    # 生成邮件内容
    def makeMail(self, mailfrom, mailto,):

        # 替换邮件内容变量
        mailbody = self.body_text
        mailbody = self.__convertCharset(mailbody, 'utf-8', self.charset)

        # 编码内容
        if self.body_code == 'base64':
            mailbody = base64.encodestring(mailbody)
        elif self.body_code == 'quoted-printable':
            mailbody = quopri.encodestring(mailbody)

        #
        # 生成新邮件
        #
        # 替换为新邮件内容
        mailfull = self.mail_orig.replace(self.body_orig, mailbody)

        # 生成邮件对象
        obj = email.message_from_string(mailfull)

        # 替换邮件头中的各字段
        # self.add_or_replace_header(obj, 'Message-Id', self.__makeMsgId())
        ### eml格式模板不替换主题 ###
        # obj.replace_header('Subject', subject)
        obj.replace_header('Date', self.mail_date)
        obj.replace_header('To', self.__makeEncodeAddr(mailto))
        # obj.replace_header('From', mailfrom)
        # obj.add_or_replace_header('Disposition-Notification-To', mailfrom)
        # obj.add_header('Mail-ID', str(uuid.uuid1()))
        return obj.as_string()

    def add_or_replace_header(self, obj, value, key):
        if obj.get(value, None) is None:
            obj.add_header(value, key)
        else:
            obj.replace_header(value, key)