# -*- coding: utf-8 -*-

import smtplib

def send_email(host, port, sender, password, receiver, message, ssl=False, debug=False):
    try:
        if ssl:
            s = smtplib.SMTP_SSL(host, port or 465)  # 发件人邮箱中的SMTP服务器，端口是25
        else:
            s = smtplib.SMTP(host, port or 25)
        if debug:
            s.set_debuglevel(1)
        code, msg = s.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        if not (200 <= code <= 299):
            return code, msg
        s.sendmail(sender, [receiver, ], message)  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        s.quit()  # 关闭连接
        return 250, 'ok'
    except smtplib.SMTPResponseException as e:
        code, msg = e.smtp_code, e.smtp_error
        return code, msg
    except smtplib.SMTPRecipientsRefused as e:
        senderrs = e.recipients
        code, msg = senderrs[receiver]
        return code, msg
    except BaseException as e:
        code, msg = -1, repr(e)
        return code, msg

import smtplib
from email.mime.text import MIMEText

class MailSender(object):
    def set_message(self, sender, receiver, subject, html_text):
        m = MIMEText(html_text, _subtype='html',_charset='gb2312')
        m['From'] = sender
        m['To'] = receiver
        m['Subject'] = subject

        return m.as_string()

    def send_email(self, host, port, sender, password, receiver, subject, message, ssl=False, debug=False):
        try:
            message = self.set_message(sender, receiver, subject, message)
            if ssl:
                s = smtplib.SMTP_SSL(host, port or 465)  # 发件人邮箱中的SMTP服务器，端口是25
            else:
                s = smtplib.SMTP(host, port or 25)
            if debug:
                s.set_debuglevel(1)

            code, msg = s.login(sender, password)
            if not (200 <= code <= 299):
                return code, msg

            s.sendmail(sender, receiver, message)
            s.quit()
            return 250, 'ok'
        except smtplib.SMTPResponseException as e:
            code, msg = e.smtp_code, e.smtp_error
            return code, msg
        except smtplib.SMTPRecipientsRefused as e:
            senderrs = e.recipients
            code, msg = senderrs[receiver]
            return code, msg
        except BaseException as e:
            code, msg = -1, repr(e)
            return code, msg
