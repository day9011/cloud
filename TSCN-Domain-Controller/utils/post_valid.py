#!/usr/bin/env python2.7
#coding=utf-8
# Name: post_valid
# Function: check post value
# Date: 2016-06-12
# Email: day9011@gmail.com
__author__ = 'day9011'

__all__ = ['DataIsValid', 'Arg']

def DataIsValid(Args, request):
    ret = {}
    print request.values
    try:
        for item in Args:
            if item['required']:
                if item['key'] in request.form:
                    t = request.form[item['key']]
                else:
                    e = "lack %s key" % (item['key'])
                    raise Exception(e)
                ret[item['key']] = t
        return 0, ret
    except Exception, e:
        return -120, str(e)

def Arg(key, required=False, default='', help=''):
    arg = {
        'key': key,
        'required': required,
        'default': default,
        'help': help
    }
    return arg