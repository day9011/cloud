# -*- coding:utf-8 -*-
__author__ = 'liming'
import threading

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):

        with self.lock:
            # print 'start thread %s' % name
            self.active.append(name)
    def makeInactive(self, name):

        with self.lock:
            # print 'stop thread %s' % name
            self.active.remove(name)


def worker(s, pool, func):

    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        func()
        pool.makeInactive(name)