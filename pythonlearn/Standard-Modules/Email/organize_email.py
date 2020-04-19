#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C)  2016 By Alex Yang.  All rights reserved.
@author : Alex Yang
@version: 1.0
@created: 2016-09-22
'''

import os
import re
import time
import urllib
import random
import string
from email import Utils, Encoders
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.header import Header

ATTACH_SAVE_PATH = os.path.realpath(os.path.dirname(__file__))

CHARS = string.lowercase + string.digits

def safe_format(template, **kwargs):
    def replace(mo):
        name = mo.group('name')
        if name in kwargs:
            return unicode(kwargs[name])
        else:
            return mo.group()

    p = r'\{(?P<name>\w+)\}'
    return re.sub(p, replace, template)

#############################################
### 通过邮件模板构造一个可以发送html、纯文本、附件的邮件 ###
class OrgEmailTemplate(object):
    def __init__(self,
                 character='utf-8', encoding='base64',
                 mail_from=u'system@bestedm.org', mail_to=u'test@bestedm.org', reply_to=None,
                 subject=None, content=None, text_content=None,
                 attachment=None,
                 replace=False,
                 is_need_receipt=False,
                 replace_domain=None,
                 sys_track_domain=None,
                 edm_check_result=None,
                 user_id=None, task_id=None ):
        """
        :param character:    设置发送编码(转换字符集)
        :param encoding:     设置邮件编码(附件编码)
        :param mail_from:    发件人
        :param mail_to:      收件人
        :param reply_to:     指定回复人
        :param subject:      主题
        :param content:      html内容
        :param text_content: 纯文本
        :param attachment:   附件信息，字典列表, 格式：[{'filepath': 'XXX', 'filetype': 'application/octet-stream', 'filename': 'xxx.txt'},...]  # [(filepath, filetype, filename, )]
        :param replace:      变量替换标志
        :param replace_domain:       链接域名替换
        :param is_need_receipt:      是否需要回执
        :param edm_check_result:      垃圾检测结果
        :param user_id:      内容额外的参数1
        :param task_id:      内容额外的参数2
        :return:             返回邮件信息
        """
        character = character or 'utf-8'
        encoding = encoding or 'base64'
        self.character = character
        self.encoding = encoding
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.reply_to = reply_to
        self.replace = replace
        self.is_need_receipt = is_need_receipt
        self.replace_domain = replace_domain
        self.sys_track_domain = sys_track_domain or []
        self.edm_check_result = edm_check_result
        self.user_id = user_id
        self.task_id = task_id

        replace_kwargs = dict()
        replace_kwargs.update(FULLNAME='name1', AREA=u'深圳福田')
        self.kwargs = replace_kwargs

        self.subject = safe_format(subject, **self.kwargs)

        self.content = self.__content_relace(content)

        text_content = text_content or u'''如果邮件内容无法正常显示请以超文本格式显示HTML邮件！\n
        （If the content of the message does not display properly, please display the HTML message in hypertext format!）'''
        self.text_content = text_content

        self.attachment = attachment or []
        self.message = MIMEMultipart('alternative')

    def __call__(self, *args, **kwargs):
        """
        # 发送一个包含纯文本、html和附件邮件：
        # 发送成功少纯文本的内容，代码没有报错，把其他的代码注掉仅发送纯文本内容，纯文本中的内容在邮件中是能看到的。
        """
        self.__make_header()
        self.__make_content()
        self.__make_attach()
        return self.message.as_string()

    def __content_relace(self, content):
        content = content.replace("\r\n", "\n")
        if self.user_id:
            content = self.__quote_replace(content, '{USER_ID}', self.user_id)
        if self.task_id:
            content = self.__quote_replace(content, '{TASK_ID}', self.task_id)

        if self.replace_domain:
            content = self.__replace_href(content)
            content = self.__replace_src(content)
        return content

    def __quote_replace(self, content, s, replace_s):
        content = content.replace(s, str(replace_s))
        content = content.replace(urllib.quote_plus(s), str(replace_s))
        return content

    # 生成一个start-end　随机长度的字符
    __make_rand_chars = lambda self, start=5, end=10: "".join(random.sample(CHARS, random.randint(start, end)))

    # 内容里面链接替换成客户的域名
    def __replace_href(self, content):
        def encrypt_url(matched):
            domain = '{}.{}'.format(self.__make_rand_chars(), self.replace_domain)
            search_url = matched.group(1)
            if search_url.startswith('http://'):
                search_url2 = (search_url.replace('http://', '')).split('/')[0]
                search_url2 = 'http://{}'.format(search_url2)
                if search_url2 in self.sys_track_domain:
                    search_url = search_url.replace(search_url2, 'http://{}'.format(domain))
            return 'href="{}"'.format(search_url)
        return re.sub('href="?\'?([^"\'>]*)', encrypt_url, content)

    # 图片链接替换
    def __replace_src(self, content):
        def encrypt_url(matched):
            domain = '{}.{}'.format(self.__make_rand_chars(), self.replace_domain)
            search_url = matched.group(1)
            if search_url.startswith('http://'):
                search_url2 = (search_url.replace('http://', '')).split('/')[0]
                search_url2 = 'http://{}'.format(search_url2)
                if search_url2 in self.sys_track_domain:
                    search_url = search_url.replace(search_url2, 'http://{}'.format(domain))
            return 'src="{}"'.format(search_url)
        return re.sub('src="?\'?([^"\'>]*)', encrypt_url, content)

    # 生成一个长度为n的数字串
    __make_rand_nums = lambda self, n=10: "".join([str(random.randint(0, 9)) for i in range(n)])

    # 生成 Message-Id
    def _makeMsgId(self):
        msgid_stat = random.randint(1,10000)
        user_id = random.randint(1,10000)
        msgid_domain = self.mail_from.split('@')[-1]
        task_ident = '{}-{}-{}'.format(time.strftime('%Y%m%d%H%M%S'), user_id, random.randint(10, 100))
        msg_id = "<%s.{RANDOM}-{%s:%s}-{COUNT}@{DOMAIN}>" % (time.strftime("%Y%m%d%H%M%S"), user_id, task_ident)
        msg_id = msg_id.replace('{COUNT}', "%07d" % msgid_stat)
        msg_id = msg_id.replace('{RANDOM}', self.__make_rand_nums(5))
        msg_id = msg_id.replace('{DOMAIN}', msgid_domain)
        return msg_id

    ######################################################
    def __make_header(self):
        # Header
        from email import utils
        # self.message['Message-Id'] = Header(self._makeMsgId(), self.character)
        self.message['Message-Id'] = Header(Utils.make_msgid(), self.character)
        if self.reply_to:
            self.message['Reply-to'] = Header(self.reply_to, self.character)
        self.message['Subject'] = Header(self.subject, self.character)
        self.message['From'] = Header(self.mail_from, self.character)
        self.message['To'] = Header(self.mail_to, self.character)
        self.message["Date"] = Utils.formatdate(localtime=True)
        if self.is_need_receipt:
            self.message['Disposition-Notification-To'] = Header(self.mail_from, self.character)
        if self.edm_check_result:
            self.message['Edm-Check-Result'] = Header(self.edm_check_result, self.character)

    def __make_content(self):
        # html或纯文本
        if self.text_content:
            part2 = MIMEText(self.text_content, 'plain', self.character)
            self.message.attach(part2)
        if self.content:
            part1 = MIMEText(self.content, 'html', self.character)
            self.message.attach(part1)

    def __make_attach(self):
        # 添加附件
        for filename, filetype, attchname in self.attachment:
            try:
                attach_file = os.path.join(ATTACH_SAVE_PATH, filename.encode('utf-8'))
                attachment = MIMEText(open(attach_file, 'r').read(), self.encoding, self.character)
                attachment['Content-Type'] = filetype
                attachment['Content-Disposition'] = 'attachment;filename="%s"' % Header(attchname, self.character)
                self.message.attach(attachment)
            except:
                continue
                # import mimetypes
                # for filepath, filetype, filename in self.attachment:
                # attach_file = os.path.join(ATTACH_SAVE_PATH, filepath.encode('utf-8'))
                # if os.path.isfile(attach_file):
                #     fd = open(attach_file, 'rb')
                #     try:
                #         mimetype, mimeencoding = mimetypes.guess_type(attach_file)
                #         if mimeencoding or (mimetype is None):
                #             mimetype = 'application/octet-stream'
                #         maintype, subtype = mimetype.split('/')
                #         if maintype == 'text':
                #             attachment = MIMEText(fd.read(), _subtype=subtype)
                #         else:
                #             attachment = MIMEBase(maintype, subtype)
                #             attachment.set_payload(fd.read())
                #             Encoders.encode_base64(attachment)
                #         attachment.add_header('Content-Disposition', 'attachment', filename=Header(filename, self.character))
                #         self.message.attach(attachment)
                #     finally:
                #         fd.close()

if __name__ == '__main__':
    def send():
        import smtplib
        import traceback

        From ='XXXXXXXXXX@qq.com'    # 发件人邮箱账号
        Passwd = 'XXXXXXXXXXXXXXXXX'              # 发件人邮箱密码
        To = '1@qq.com'      # 收件人邮箱账号，我这边发送给自己

        subject = u"菜鸟教程发送邮件测试"
        content = u"填写邮件内容"

        attachment = [
            ('test.eml', 'application/octet-stream', u'测试邮单方事故会fdsgfd计法厚大司考浩丰科技倒#$%顺-)()开关^&符合!~贷款改好了客服电话看了2018件.eml')
        ]
        msg = OrgEmailTemplate(
            mail_from=From, mail_to=To, subject=subject, content=content, attachment=attachment
        )()

        try:
            server=smtplib.SMTP_SSL("mail2.comingchina.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.set_debuglevel(1)
            server.login(From, Passwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(From, [To, ], msg)  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            return True
        except BaseException as e:
            print traceback.format_exc(e)
        return False

    send()


