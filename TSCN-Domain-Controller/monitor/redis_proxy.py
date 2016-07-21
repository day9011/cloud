# -*- coding:utf-8 -*-
__author__ = 'liming'
from redis import Redis

from auth import get as auth_get


class redis_proxy(object):

    def __init__(self):

        self.c = Redis(host=auth_get('redis_host'), port=auth_get('redis_port'),
                       db=auth_get('redis_db'), password=auth_get('redis_pass'))

    def get(self, k):
        return self.c.get(k)

    def set(self, k, v, ttl=None):
        s = self.c.set(k, v, ex=ttl)
        return s