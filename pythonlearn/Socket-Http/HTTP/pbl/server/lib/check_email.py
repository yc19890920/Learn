#!/usr/bin/python
#coding=utf8
import getopt
import imaplib
import re
import redis
import sys
import requests

__author__ = 'leo'


def worker(options):

    M = imaplib.IMAP4(host=options['MAIL_HOST'])
    M.login(options['MAIL_ADDRESS'], options['MAIL_PASSWORD'])
    M.select(readonly=True)
    typ, data = M.search(None, 'ALL')

    url_list = []
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        # print 'Message %s\n%s\n' % (num, data[0][1])
        url = re.findall(r"(http://www.spamhaus.org/pbl/removal/verify/[_0-9]+)", data[0][1])
        if url:
            url_list.append(url[0])

    M.close()
    M.logout()

    pool = redis.ConnectionPool(host=options['REDIS_DB_HOST'], port=options['REDIS_DB_PORT'],
                                db=options['REDIS_DB_NAME'])
    cli = redis.Redis(connection_pool=pool)

    for url in url_list:
        while True:
            try:
                requests.get(url)
                cli.sadd('email_check', url)
                break
            except requests.exceptions.RequestException as e:
                try:
                    requests.post('http://%s:%s/report' % (options['WEB_SERVER_IP'], options['PORT']), data={"info": "check email url Error:" + e.message})
                except requests.exceptions.RequestException as e:
                    print "Critical Error"
                    continue

    requests.post('http://%s:%s/report'% (options['WEB_SERVER_IP'], options['PORT']), data={"info": "check email: url... "})
    pool.disconnect()


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["MAIL_HOST=", "MAIL_ADDRESS=", "MAIL_PASSWORD=",
                                                      "REDIS_DB_HOST=", "REDIS_DB_PORT=", "REDIS_DB_NAME=", "WEB_SERVER_IP=", "PORT="])
    except getopt.GetoptError as err:
        print "check_email script parse argument error"
        sys.exit(0)

    options = {}
    for k, v in opts:
        k = k.strip("--")
        if k == "REDIS_DB_PORT":
            options[k] = int(v)
        else:
            options[k] = v

    worker(options)
