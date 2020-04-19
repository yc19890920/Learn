# -*- coding: utf-8 -*-
#
__author__ = 'leo, yc'

import os
import re
import sys
import time
import datetime
import traceback
from js2py import eval_js
from email.parser import Parser
from imapclient import IMAPClient
from gevent.coros import BoundedSemaphore

from pbl_configs import HOST, HEADERS, MAIL_ADDRESS, MAIL_PASSWD, MAIL_IMAP_HOSTNAME
from DeathByCaptcha import SocketClient
from parse_email import ParseEmail

#设定对共享资源的访问数量
#  only allows 1 greenlets at one time, others must wait until one is released
sem = BoundedSemaphore(1)

def check_ip(session, ip):
    # r = session.get('http://www.spamhaus.org/lookup/ip/?ip=%s' % ip)
    # session.headers.update({'Referer': 'http://www.spamhaus.org/lookup/ip/?ip=%s' % ip})
    content = retry_check_ip(session, ip)
    with open("/home/python/ttt/pbl_killer/client/chk_jschl.html", 'wb+') as f:
        f.write(content)

    PBL, SBL, XBL = '-1', '-1', '-1'
    if content.find("is listed in the PBL") > 0:
        PBL = '1'
    if content.find("is listed in the SBL") > 0:
        SBL = '1'
    if content.find("is listed in the XBL") > 0:
        XBL = '1'

    return PBL, SBL, XBL, content

def retry_check_ip(session, ip):
    count = 5
    while count>0:
        try:
            r = session.get('https://www.spamhaus.org/lookup/ip/?ip=%s' % ip)
            session.headers.update({'Referer': 'https://www.spamhaus.org/lookup/ip/?ip=%s' % ip})

            jschl_vc, passwd, jschl_answer = get_js_return(r.content)

            payload = {'jschl_vc': jschl_vc, 'pass': passwd, 'jschl_answer': jschl_answer}

            time.sleep(4)

            r = session.get("https://www.spamhaus.org/cdn-cgi/l/chk_jschl?", params=payload)

            r = session.get('https://www.spamhaus.org/lookup/ip/?ip=%s' % ip)

            return r.content
        except BaseException as e:
            print >> sys.stderr, 'Error get_js_return retry={}...'.format(count)
            print >> sys.stderr, traceback.format_exc()
            count -= 1
            time.sleep(1)
    return ""


def get_captcha_code(session, captcha_file_path):
    client = SocketClient('Shoufeng', 'Shoufeng#123')
    client.is_verbose = False

    info = 'Your balance is %s US cents' % client.get_balance()
    print >> sys.stderr, info

    try:
        captcha = client.decode(captcha_file_path)
    except Exception, e:
        return False, e.message

    if captcha:
        return True, captcha['text']
    return False, "No text"


def get_captcha_pic(session, url):
    """
    获取验证码图片放/tmp目录
    """
    local_filename = url.split('/')[-1]

    file_path = os.path.join('/tmp/', local_filename)

    r = session.get(url, stream=True)

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return file_path

def get_js_return(content):
    """
    <form id="challenge-form" action="/cdn-cgi/l/chk_jschl" method="get">
        <input type="hidden" name="jschl_vc" value="53c6b5dc36c113610e2597f11d600d1a"/>
        <input type="hidden" name="pass" value="1504765865.161-4zOzo1BY22"/>
        <input type="hidden" id="jschl-answer" name="jschl_answer"/>
    </form>
    """
    # 1ac9690a11b8fcfca762bc36f64679f9, 1504779184.092-aYUwU2JqVN, 2032
    # __cfduid    de7bab0aaae0290de0540da8fba78f3731504779180
    # cf_clearance   dc3e9630656b5528c0f1c10d7c9c523c7606e096-1504779185-28800

    jschl_vc = "0f7e4868294108cd97d299fba2b793a6"
    passwd = "1504832239.691-38r4axZu7r"
    jschl_answer = "1875"

    l = re.findall(r'name="jschl_vc" value="(.*?)"', content)
    if l: jschl_vc = l[0]

    l = re.findall(r'name="pass" value="(.*?)"', content)
    if l: passwd = l[0]

    m = re.search(r'setTimeout\(function\(\)\{((?:.|\n)*?)f\.submit\(\)', content)
    if m:
        s = m.group(1)
        l = s.split("\n")
        l = [i for i in l if i.split()]
        first = l[0]
        last = l[-1]
        _ret = re.search(r"(.*?)a\.value\s+=\s+((.*?)121')", last)
        if _ret:
            last = _ret.group(1)
            ret = _ret.group(2)
        js = "function f(){ %s  %s  %s  return %s }" % (
            first,
            """
            t = 'https://www.spamhaus.org/';
            r = t.match(/https?:\/\//)[0];
            t = t.substr(r.length); t = t.substr(0,t.length-1);
          """,
            last,
            ret
        )
        jschl_answer = eval_js(js)()
    return jschl_vc, passwd, jschl_answer

def retry_process(session):
    count = 5
    while count>0:
        try:
            r = session.get('https://www.spamhaus.org/pbl/removal/',  headers=HEADERS)

            jschl_vc, passwd, jschl_answer = get_js_return(r.content)

            payload = {'jschl_vc': jschl_vc, 'pass': passwd, 'jschl_answer': jschl_answer}

            time.sleep(4)

            r = session.get("https://www.spamhaus.org/cdn-cgi/l/chk_jschl?", params=payload)

            r = session.get('https://www.spamhaus.org/pbl/removal/',  headers=HEADERS)

            agree_code = re.findall(r'name="code" value="(.*?)"', r.content)[0]
            return session, agree_code
        except BaseException as e:
            print >> sys.stderr, 'Error get_js_return retry={}...'.format(count)
            print >> sys.stderr, traceback.format_exc()
            count -= 1
            time.sleep(1)
    return session, None

def process(session, ip, email):
    """
    同意协议，请求表单和验证码，解析验证码，提交表单
    """
    # r = session.get('http://www.spamhaus.org/pbl/removal/',  headers=HEADERS)
    # agree_code = re.findall(r'name="code" value="(.*?)"', r.content)[0]

    session, agree_code = retry_process(session)
    r = session.post('https://www.spamhaus.org/pbl/removal/form/',
                     data={'code': agree_code, 'accept': 'yes'},
                     headers=HEADERS)

    # print '22222222222', r.request.headers
    # 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect',
    # 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', '
    # ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url'

    form_code = re.findall(r'name="code" value="(.*?)"', r.content)[0]
    print >> sys.stdout, 'Success get_js_return...'

    # 获取验证码图片
    captcha_file_path = get_captcha_pic(session, 'https://www.spamhaus.org/pbl/util/captcha.jpg')

    # 获取验证内容
    flag, info = get_captcha_code(session, captcha_file_path)
    if flag:
        captcha_code = info
    else:
        return False, info

    # 提交清除申请
    data = {'code': form_code, 'ip_addr': ip, 'email': email,
            'country': 'CN', 'iptype': 'STATIC', 'ipbelongs': 'SERVER',
            'test': captcha_code, '-nothing': 'Submit'}
    time.sleep(10)
    r = session.post('https://www.spamhaus.org/pbl/removal/process/', data=data)
    print >> sys.stdout, 'data: %s' % data
    # print '1111111111111111111', r.request.headers
    removal_code = re.findall(r'name="removal" value="(.*?)"', r.text)
    if not removal_code:
        removal_code = re.findall(r"name='removal' value='(.*?)'", r.text)
    removal_code = removal_code[0]

    # 获取邮件验证码 并提交表单
    # 暂停30秒 再去查看邮件
    time.sleep(30)
    auth_code = get_email_code(ip)
    data = {
        "removal": removal_code,
        "auth": auth_code,
        "-nothing": "Finish",
    }
    r = session.post('https://www.spamhaus.org/pbl/removal/verify/', data=data)
    if r.status_code == 200:
        with open('/tmp/%s'%ip, 'wb') as f:
            f.write(r.text)
        return True, u"完成'%s'PBL清除表单提交" % ip
    else:
        return False, u"'%s'PBL清除表单提交异常" % ip

def get_email_code(ip):
    with sem:
        server = IMAPClient(MAIL_IMAP_HOSTNAME)
        try:
            server.login(MAIL_ADDRESS, MAIL_PASSWD)
            server.select_folder('INBOX')
            _before = datetime.datetime.now() - datetime.timedelta(minutes=15)
            result = server.search(['UNSEEN', 'SINCE', _before])
            msgdict = server.fetch(result, ['BODY.PEEK[]'] )
            msgtuple=sorted(msgdict.items(), key=lambda e:e[0], reverse=True)
            for message_id, message in msgtuple:
                msg_content = message['BODY[]']
                auth_code = do_email(msg_content, ip)
                if auth_code:
                    server.add_flags(message_id, '\\seen')
                    return auth_code
        finally:
            server.logout()

def do_email(msg_content, ip):
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    email_str = msg.as_string()
    p = ParseEmail(email_str)
    m = p.parseMailTemplate()
    text = m.get('html_text', '').strip()
    if not text: text = m.get('plain_text', '')
    ip_info = "IP Address {} from the Spamhaus PBL database".format(ip)
    if text.find(ip_info) > 0:
        m = re.search(r"Verification/Confirmation Code:\s+(\d+)", text)
        if m: return m.group(1)
    return None

if __name__ == "__main__":
    # bind_ip_test()

    print get_captcha_code('/home/leo/Desktop/captcha.jpg')
