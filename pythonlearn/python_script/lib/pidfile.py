#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pid file manager
"""

import os
import sys
import fcntl
import atexit


def register_pidfile(pidfile):
    try:
        fd = os.open(pidfile, os.O_RDWR|os.O_CREAT|os.O_NONBLOCK|os.O_DSYNC)
        fcntl.flock(fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        os.write(fd, str(os.getpid()))
        atexit.register(clear_pidfile, pidfile=pidfile)

    except (OSError, IOError), e:
        if e.errno in (35, 11):
            print >> sys.stderr, '%s already running: pid=%s' % (' '.join(sys.argv), open(pidfile).read())
        else:
            print >> sys.stderr, e

        sys.exit(-1)


def clear_pidfile(pidfile):
    if os.path.exists(pidfile):
        try:
            os.unlink(pidfile)
        except OSError:
            pass


if __name__ == '__main__':
    register_pidfile('test.pid')
    print 'pid=%s, running...' % os.getpid()
    import time
    while True:
        time.sleep(1)
