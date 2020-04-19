# -*- coding: utf-8 -*-
#

import sys
import re
import dkim
import base64
import rsa
import traceback
import email
import time

import dns.resolver
dns.resolver.get_default_resolver().cache = dns.resolver.LRUCache()


############################################################
# 查询dns记录
def try_query(qname, rdtype):
    try:
        rs = []
        answers = dns.resolver.query(qname, rdtype)
        for a in answers:
            if rdtype == 'mx':
                rs.append(a.exchange.to_text())
            elif rdtype in ['txt', 'cname']:
                rs.append(a.to_text())
            else:
                rs.append(a)
        return rs
    except dns.exception.DNSException:
        return []

def valid_domain(domain, rdtype, record='', dkim_selector='umail'):
    """
    检测域名记录
    :param domain: 域名
    :param rdtype: 检测类型 mx, spf, dkim
    :param record: 数据库的记录
    :return:
    """
    if rdtype == 'spf':
        t_record = try_query(domain, 'txt')
        return t_record[0].find(record) != -1 if t_record else False
    if rdtype == 'mx':
        t_record = try_query(domain, 'mx')
        return record in t_record or '{}.'.format(record) in t_record
    if rdtype == 'dkim':
        t_record = try_query('{}._domainkey.{}'.format(dkim_selector, domain), 'txt')
        return t_record[0][1:-1] == record if t_record else False
    if rdtype == 'cname':
        t_record = try_query(domain, 'cname')
        return t_record[0].find(record) != -1 if t_record else False



############################################################
# dkim
def get_dkim_info(domain):
    selector = 'umail'
    private = """-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCWE8IMzZX7lr24GRubcB9GdzYTW/4l7"""
    return selector, private
    # rs = DB.query("select selector, private from core_dkim where domain=%s and status=1", (domain,))
    # return rs[0] if rs else None


def nofws(message, include_heads):
    """
    No Folding Whitespace
    参考: http://tools.ietf.org/html/rfc4870#page-19
    """
    headers, body = dkim.rfc822_parse(message)
    headers_dict = dict(headers)

    heads = ['%s:%s' % (k, re.sub('\s', '', v)) for k, v in headers_dict.items() if k in include_heads]

    data = '\n'.join(heads) + '\n'

    for e in ('\n' + body.replace('\r', '')).split('\n'):
        data += re.sub('\s', '', e) + '\n'

    data = data.rstrip('\n').split('\n')
    data = '\r\n'.join(data) + '\r\n'

    return data


def domainkeys(message, selector, domain, private_key, include_heads=['From', 'To', 'Subject', 'Date']):
    try:
        message = nofws(message, include_heads)
        sig = base64.b64encode(rsa.sign(message, rsa.PrivateKey.load_pkcs1(private_key), 'SHA-1'))
        return 'DomainKey-Signature: a=rsa-sha1; s={selector}; d={domain}; c=nofws; q=dns; h={include_heads}; ' \
               '\r\n b={sig};\r\n'.format(selector=selector, domain=domain,
                                          sig=sig, include_heads=':'.join(include_heads))
    except Exception, e:
        print >>sys.stderr, e
        print >>sys.stderr, traceback.format_exc()
        return ''


def repalce_mail(content, sender):
    mail_obj = email.message_from_string(content)
    try:
        mail_obj.replace_header('Sender', sender)
    except:
        mail_obj.add_header('Sender', sender)

    mail_date = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    try:
        mail_obj.replace_header('Date', mail_date)
    except:
        mail_obj.add_header('Date', mail_date)
    return mail_obj.as_string()


def gen_mail_content(content, addr_from):
    """
    根据邮件体生成添加了dkim的新邮件
    @param content: string 邮件体内容
    @return str_mail: 加上dkim的新邮件
    """
    try:
        domain = addr_from.split('@')[-1]
        dkim_info = get_dkim_info(domain)
        if dkim_info:
            content = repalce_mail(content, addr_from)
            selector, private = dkim_info
            private = private.replace('\r\n', '\n')
            dkim_sig = dkim.sign(content, selector, domain, private, include_headers=['From', 'To', 'Subject', 'Date'])
            dk_sig = domainkeys(dkim_sig + content, selector, domain, private, include_heads=['From', 'To', 'Subject'])
            return dk_sig + dkim_sig + content
        else:
            return content
    except Exception, e:
        print >>sys.stderr, e
        print >>sys.stderr, traceback.format_exc()
        return content

