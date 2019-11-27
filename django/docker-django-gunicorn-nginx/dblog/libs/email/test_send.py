# -*- coding: utf-8 -*-


if __name__ == '__main__':
    print '-------------1'
    import send_email

    HOST = 'smtp.qq.com'
    PORT = 465
    From ='1793302800@qq.com'    # 发件人邮箱账号
    Passwd = 'marxkarlmmx'              # 发件人邮箱密码
    SSL = True

    HOST = "mail2.comingchina.com"
    PORT = 25
    From ='sent@comingchina.com'    # 发件人邮箱账号
    Passwd = '5rdxCFG.,m87SS'              # 发件人邮箱密码
    SSL = False

    To = '2948906420@qq.com'      # 收件人邮箱账号，我这边发送给自己


    subject = u"这是一个测试"
    content = u"这是一个测试"
    s = send_email.MailSender()
    code,msg = s.send_email(HOST, PORT, From, Passwd, To, subject, content, ssl=SSL, debug=True)
    print '-------------2', code,msg