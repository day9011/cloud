# -*- coding:utf-8 -*-
__author__ = 'liming'
from redis import Redis
from utils.auth import get as auth_get

class redis_proxy(object):

    def __init__(self):

        self.c = Redis(host=auth_get('redis_host'), port=auth_get('redis_port'),
                       db=auth_get('redis_db'), password=auth_get('redis_pass'))

    def get(self, k):
        return self.c.get(k)

    def set(self, k, v, ttl=None):
        return self.c.set(k, v, ex=ttl)

    def get_dict(self, k, name=None):
        if name is None:
            return self.c.hgetall(k)
        else:
            return self.c.hget(k, name)

    def set_dict(self, k, dict_content):
        if not isinstance(dict_content, dict):
            return False

        for _k, _v in dict_content.items():
            self.c.hset(k, _k, _v)



