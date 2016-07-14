#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 25/5/16 PM1:38
# Copyright: TradeShift.com
__author__ = 'liming'

from app.auth import get as auth_get
from redis import Redis
import logging

logger = logging.getLogger(__name__)

class RedisProxy(object):

    def __init__(self):
        self.c = None

    def _connet(self):
        if self.c is None:
            self.c = Redis(host=auth_get('redis_host'), port=auth_get('redis_port'), db=auth_get('redis_db'), password=auth_get('redis_pass'))

    def get(self, k):
        self._connet()
        return self.c.get(k)

    def set(self, k, v, ttl=None):
        self._connet()
        s = self.c.set(k, v, ex=ttl)
        return s

    def dict_set(self, k, d):
        self._connet()
        s = self.c.hmset(k ,d)
        return s