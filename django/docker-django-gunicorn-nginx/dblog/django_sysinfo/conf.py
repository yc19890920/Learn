# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings


def merge(a, b, path=None):
    """merges b into a

    >>> a={1:{"a":"A"},2:{"b":"B"}, 8:[]}
    >>> b={2:{"c":"C"},3:{"d":"D"}}

    >>> c = merge(a, b)
    >>> c == a == {8: [], 1: {"a": "A"}, 2: {"c": "C", "b": "B"}, 3: {"d": "D"}}
    True

    >>> c = merge(a, {1: "a"})
    >>> print(c[1])
    a
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
                # raise Exception("Conflict at %s (%s %s)" % (".".join(path + [str(key)]),
                # a[key], b[key]))
        else:
            a[key] = b[key]
    return a


DEFAULTS = {"_ttl": 0,
            "os": True,
            "modules": True,
            "python": True,
            "host": True,
            "extra": {},
            "checks": {},
            "installed_apps": True,
            "processes": True,
            "queues": True,
            "project": {
                "mail": True,
                "databases": True,
                "MEDIA_ROOT": True,
                "STATIC_ROOT": True,
                "CACHES": True}
}

PROCESSES = {
    'mta': {
        'cmd': '/usr/local/u-mail/service/postfix/libexec/master',
        'sname': u'MTA服务',
        'restart': '/etc/init.d/umail_postfix restart',
        'log': '/var/log/maillog',
        'order': 1
    },
    'dovecot': {
        'cmd': '/usr/local/u-mail/service/dovecot/sbin/dovecot',
        'sname': u'POP、IMAP服务',
        'restart': '/etc/init.d/umail_dovecot restart',
        'order': 2
    },
    'postgrey': {
        'cmd': '/usr/local/u-mail/service/postfix/sbin/postgrey',
        'sname': u'SMTPD灰名单服务',
        'restart': '/etc/init.d/umail_postgrey restart',
        'order': 3
    },
    'sa': {
        'cmd': '/usr/local/u-mail/service/spamassassin/bin/spamd',
        'sname': u'反垃圾邮件服务(sa)',
        'restart': '/etc/init.d/umail_spamassassin restart',
        'order': 4
    },
    'dspam': {
        'cmd': '/usr/bin/dspam',
        'sname': u'反垃圾邮件服务(dspam)',
        'restart': '/etc/init.d/umail_dspam restart',
        'order': 5
    },
    'httpd': {
        'cmd': '/usr/local/u-mail/service/apache/bin/httpd',
        'sname': u'WEB应用服务(httpd)',
        'restart': '/etc/init.d/umail_apache restart',
        'log': '/usr/local/u-mail/log/apache/mail_access_log',
        'order': 6
    },
    'nginx': {
        'cmd': '/usr/local/u-mail/service/nginx/sbin/nginx',
        'sname': u'WEB应用缓存(nginx)',
        'restart': '/etc/init.d/umail_nginx restart',
        'log': '/usr/local/u-mail/log/nginx/access.log',
        'order': 7
    },
    'mysql': {
        'cmd': '/usr/local/u-mail/service/mysql/bin/mysqld',
        'sname': u'数据库(mysql)',
        'restart': '/etc/init.d/umail_mysqld restart',
        'log': '/usr/local/u-mail/log/mysql/default.err',
        'order': 8
    },
    'redis': {
        'cmd': '/usr/local/u-mail/service/redis/bin/redis-server',
        'sname': u'数据库(redis)',
        'restart': '/etc/init.d/umail_redis restart',
        'log': '/usr/local/u-mail/log/redis/redis.log',
        'order': 9
    },
    'pg': {
        'cmd': '/usr/local/u-mail/service/pgsql-9.4/bin/postmaster',
        'sname': u'数据库(Pg)',
        'restart': '/etc/init.d/umail_postgresql restart',
        'log': '/usr/local/u-mail/service/pgsql-9.4/data/pgstartup.log',
        'order': 10
    },
    'fail2ban': {
        'cmd': '/usr/bin/fail2ban-server',
        'sname': u'Fail2ban',
        'restart': '/etc/init.d/fail2ban restart',
        #'log': '/usr/local/u-mail/service/pgsql-9.4/data/pgstartup.log',
        'order': 11
    },
    'rulefilter': {
        'cmd': '/usr/local/u-mail/app/repo/rulefilter.py',
        'sname': u'Rulefilter服务',
        'restart': '/usr/local/u-mail/app/engine/bin/supervisorctl -c /usr/local/u-mail/app/conf/supervisord.ini restart rulefilter',
        'log': '/usr/local/u-mail/log/app/rulefilter.log',
        'order': 12
    },
    'receiver': {
        'cmd': '/usr/local/u-mail/app/repo/receiver.py',
        'sname': u'Receiver服务',
        'restart': '/usr/local/u-mail/app/engine/bin/supervisorctl -c /usr/local/u-mail/app/conf/supervisord.ini restart receiver',
        'log': '/usr/local/u-mail/log/app/receiver.log',
        'order': 13
    },
    'dispatcher': {
        'cmd': '/usr/local/u-mail/app/repo/dispatcher.py',
        'sname': u'Dispatcher服务',
        'restart': '/usr/local/u-mail/app/engine/bin/supervisorctl -c /usr/local/u-mail/app/conf/supervisord.ini restart dispatcher',
        'log': '/usr/local/u-mail/log/app/dispatcher.log',
        'order': 14
    },
    'sizequerier': {
        'cmd': '/usr/local/u-mail/app/repo/sizequerier.py',
        'sname': u'Sizequerier服务',
        'restart': '/usr/local/u-mail/app/engine/bin/supervisorctl -c /usr/local/u-mail/app/conf/supervisord.ini restart sizequerier',
        'log': '/usr/local/u-mail/log/app/sizequerier.log',
        'order': 15
    },
    'auth': {
        'cmd': '/usr/local/u-mail/app/repo/authenticator.py',
        'sname': u'Auth服务',
        'restart': '/usr/local/u-mail/app/engine/bin/supervisorctl -c /usr/local/u-mail/app/conf/supervisord.ini restart authenticator',
        'log': '/usr/local/u-mail/log/app/authenticator.log',
        'order': 16
    },
}

class Config(object):
    """
    >>> c = Config({"os": True})
    >>> c.os, c.python
    (True, False)
    >>> c = Config({"os": True, "project": False})
    >>> c.project
    False

    """

    def __init__(self, config):
        self._config = DEFAULTS.copy()
        merge(self._config, config)

    @property
    def ttl(self):
        return int(self._ttl)

    def __getattr__(self, item):
        if item in self._config:
            return self._config[item]
        elif item in self._config["project"]:
            if not self._config["project"]:
                return False
            return self._config["project"][item]
        return None
        # raise AttributeError("Config does not have attribute {}".format(item))

    def __repr__(self):
        return str({"host": self.host,
                    "os": self.os,
                    "processes": self.processes,
                    "queues": self.queues,
                    "mail": self.mail,
                    "python": self.python,
                    "modules": self.modules,
                    "project": self.project,
                    "databases": self.databases,
                    "installed_apps": self.installed_apps,
                    "extra": self.extra
        })


config = Config(getattr(settings, "SYSINFO", {}))
