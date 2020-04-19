#!/usr/bin/python
#coding=utf8
import email
from email.header import decode_header
import imaplib
import re

__author__ = 'leo'

SUBJECT = []

def worker():
    # 192.168.1.72 test@domain.com 1qaz2wsx
    M = imaplib.IMAP4(host='192.168.1.72')
    M.login('test@domain.com', '1qaz2wsx')
    M.select(readonly=True)
    typ, data = M.search(None, 'ALL')
    print len(data[0])

    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        if typ == 'OK':
            mail_obj = email.message_from_string(data[0][1])
            subject_head = dict(mail_obj._headers).get('Subject', False)

            # subject, encode_type = decode_header(subject_head)[0]
            #
            # if encode_type:
            #     subject = subject.decode(encode_type)
            #     print num, subject
            if subject_head not in SUBJECT:
                SUBJECT.append(subject_head)
            else:
                # M.delete(num)
                print "delete ", num
                M.store(num, '+FLAGS', '\\Deleted')
    M.expunge()

    M.logout()



if __name__ == "__main__":
    worker()
