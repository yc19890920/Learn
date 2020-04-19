# -*- coding: utf-8 -*-

import smtplib

def send_email(host, port, sender, password, receiver, message, ssl=False, debug=False):
    try:
        if ssl:
            print port
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

if __name__ == '__main__':
    import make_email

    HOST = 'mail2.comingchina.com'
    PORT = 465
    From ='yc@comingchina.com'    # 发件人邮箱账号
    Passwd = '9ijn*UHBvc'              # 发件人邮箱密码
    To = '1793302800@qq.com'      # 收件人邮箱账号，我这边发送给自己
    # To = '1248644045@qq.com'
    # To = "18924664854@163.com"
    # To = "circle811@gmail.com"
    To = "ysqzx6388260@gmail.com" # lanlan1248644045

    # HOST = "mail2.comingchina.com"
    # PORT = 465
    # FROM = "sent@comingchina.com"
    # Passwd = "5rdxCFG.,m87SS"
    ssl = True

    ssl = False
    HOST, PORT, From, Passwd = "mail2.comingchina.com", 25, "sent@comingchina.com", "5rdxCFG.,m87SS"
    PORT = 465
    ssl = True
    # From ='yc@comingchina.com'    # 发件人邮箱账号
    # Passwd = '9ijn*UHBvc'              # 发件人邮箱密码



    subject = u"这是一个测试"
    content = u"这是一个测试"
    # # attachment = [
    # #     ('test.eml', 'application/octet-stream', u'测试邮单方事故会fdsgfd计法厚大司考浩丰科技倒#$%顺-)()开关^&符合!~贷款改好了客服电话看了2018件.eml')
    # # ]
    attachment = []
    msg = make_email.OrgEmailTemplate(
        mail_from=From, mail_to=To, subject=subject, content=content, attachment=attachment
    )()

    import replace_email
    # with open("test.eml", "r") as f:
    #     content = f.read()
    # r = replace_email.ReplaceEmail(content)
    # msg = r.makeMail(From, To)
    code, msg = send_email(HOST, PORT, From, Passwd, To, msg, ssl=ssl, debug=False)
    print '----------------------'
    print code, msg

    # from unsubscribe import UnsubscribableEmailMessage


