#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 16/5/16 PM4:11
# Copyright: TradeShift.com
__author__ = 'liming'

import sys, traceback
import logging, time

logger = logging.getLogger(__name__)

def exception_2_list(f):
    def handler(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            # message = '\n{0}\n{1}:\n{2}'.format(
            #     formatted_traceback,
            #     exc_type.__name__,
            #     exc_instance
            # )
            message = '\n{0}\n{1}'.format(
                exc_type.__name__,
                exc_instance
            )
            logger.error(message)
            return []

        finally:
            pass

    return handler

def cur_time(t_stamp=None):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_stamp))

def retry(attempt):
    # decorator, need func return a status
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            result = (999, 'default error')
            while att < attempt:
                try:
                    result = func(*args, **kw)
                    # if isinstance(result, int):
                    #     status = result
                    # elif isinstance(result, tuple):
                    #     status = result[0]
                    # else:
                    #     raise Exception('Bad return format from func: %s, returns: %s' % (func, result))
                    #
                    # if status:
                    #     raise Exception('Bad status return from func: %s, returns: %s' % (func, result))
                    # else:
                    #     break
                    break
                except Exception as e:
                    logger.warning('Error in retry: %s' % str(e.args))
                    att += 1
                    time.sleep(0.5)
            return result
        return wrapper
    return decorator