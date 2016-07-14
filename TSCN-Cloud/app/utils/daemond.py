# -*- coding:utf-8 -*-
__author__ = 'liming'
import os, sys

def be_daemon():
    """
    Fork a daemon who will do the rest of parent's job, and parent quit.

    It looks like you are being a daemon.
    """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, 'fork #1 failed: %d (%s)' % (
            e.errno, e.strerror)
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    # Second fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, 'fork #2 failed: %d (%s)' % (
            e.errno, e.strerror)
        sys.exit(1)