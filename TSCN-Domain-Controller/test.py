#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 29/6/16 PM5:54
# Copyright: TradeShift.com
__author__ = 'liming'

import requests, json, sys

url = 'http://127.0.0.1:9999'

def create(seq):

    uri = '/tsRole/create'
    d = {
    'seq' : seq,
    'tsRoleName' : 'web%s.bwts.ct.com' % seq,
    'roleName' : 'lmapp',
    'cpu' : 1,
    'mem' : int(0.5 * 1024 * 1024 * 1024),
    'image' : '192.168.100.2:5000/testweb:new',
    'port' : [80],
    'env' : {
	'name': 'liming',
	'lm.age': 30,
    },
    }

    r = requests.post(url + uri, {'create_value': json.dumps(d)})
    print r.json()

def delete(rid):
    uri = '/tsRole/delete'
    d = {'rsResourceId': rid}
    r = requests.post(url + uri, d)
    print r.json()

def start(rid):
    uri = '/tsRole/%s/start' % rid
    r = requests.post(url + uri)
    print r.json()

def stop(rid):
    uri = '/tsRole/%s/stop' % rid
    r = requests.post(url + uri)
    print r.json()

if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'create':
        seq = sys.argv[2]
        if not seq:
            print 'miss seq'
        else:
            create(seq)

    elif action == 'delete':
        rid = sys.argv[2]
        if not rid:
            print 'miss rid'
        else:
            delete(rid)

    elif action == 'start':
        rid = sys.argv[2]
        if not rid:
            print 'miss rid'
        else:
            start(rid)

    elif action == 'stop':
        rid = sys.argv[2]
        if not rid:
            print 'miss rid'
        else:
            stop(rid)

    else:
        print 'Bad option'