#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 18/3/16 PM12:55
# Copyright: TradeShift.com
__author__ = 'liming'
import requests
import time

def cur_time(t_stamp=None):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_stamp))

def retry(attempt):
    # decorator, need func return a status
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            result = (999, 'default')
            while att < attempt:
                try:
                    result = func(*args, **kw)
                    if isinstance(result, int):
                        status = result
                    elif isinstance(result, tuple):
                        status = result[0]
                    else:
                        raise Exception('Bad return format from func: %s, returns: %s' % (func, result))
                    if status:
                        raise Exception('Bad status return from func: %s, returns: %s' % (func, result))
                    else:
                        break
                except Exception as e:
                    # logger.warning('Error in retry: %s' % str(e.args))
                    att += 1
                    time.sleep(1)
            return result
        return wrapper
    return decorator

@retry(attempt=3)
def http_call(url, data=None, method='post'):
    methods = {'post': requests.post,
               'get': requests.get,
               'put': requests.put,
               'delete': requests.delete}
    if data is not None and not isinstance(data, dict):
        # logger.error('Bad requests parameter: url - %s, data - %s' % (url, data))
        return 1, None

    requests_func = methods.get(method)
    if requests_func is None:
        # logger.error('Bad requests method: %s' % method)
        return 1, None

    try:
        r = requests_func(url) if data is None else requests_func(url, data)
        if r.status_code != 200:
            return 2, None
        return 0, r.json()
    except Exception,e:
        # logger.error('requests exception: %s' % str(e.args))
        return 3, None
