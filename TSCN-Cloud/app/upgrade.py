#!/usr/bin/env python2.7
#coding=utf-8
# Name: upgrade
# Function: upgrade api
# Date: 2016-06-30
# Email: day9011@gmail.com
__author__ = 'day9011'


from . import app
from app.utils.db import Db_access
from flask import (request,
                   render_template,
                   make_response,
                   redirect)
import requests
from flask import json
from app.utils.gettime import get_current
import logging

logger = logging.getLogger(__name__)
db = Db_access()

@app.route('/ts/upgrade/tsRole', methods=['POST'])
def upgrade_tsRole():
    ret = {'status': 0, 'message': 'OK'}
    try:
        data = json.loads(request.get_data())
        logger.info("upgrade" + str(data))
        print data
        s, c = db.get("SELECT url FROM domain")
        if s:
            raise Exception('Get domain list fail: %s' % c)
        time = get_current()
        image = data['image'] + ':' + data['branch'] + '-' + data['tag']
        sqlstr = "SELECT a.project_id as project_id, a.domain_id as domain_id, a.role_id as role_id, a.resource_id as resource_id, a.name as tsRoleName, a.role_seq " \
                 "as seq, b.cpu as cpu, b.mem as mem, c.name as roleName, c.port as port FROM ts_role as a " \
                 "INNER JOIN project_role as b ON b.role_id=a.role_id INNER JOIN role as c ON c.id=a.role_id " \
                 "WHERE a.id=%s" % (data['ts_roleId'])
        print sqlstr
        s, f = db.get(sqlstr)
        if s:
            raise Exception("query containeid id error")
        f = f[0]
        sql_str = 'SELECT key_name as k, key_value as v FROM var_table WHERE domain_id=%s AND role_id=%s ' \
                  'AND project_id=%s;' % (f['domain_id'], f['role_id'], f['project_id'])
        s, _env = db.get(sql_str)
        if s or not _env:
            raise Exception("get env error")
        env = {}
        for item in _env:
            env[item['k']] = item['v']
        if not f['port']:
            f['port'] = []
        param = {
            'tsResourceId': f['resource_id'],
            'create_value': {
                'seq': f['seq'],
                'tsRoleName': f['tsRoleName'],
                'roleName': f['roleName'],
                'cpu': f['cpu'],
                'mem': int(f['mem']) * 1024 * 1024,
                'image': image,
                'port': f['port'],
                'env': env,
                'need_restart': int(data['restart']),
            }
        }
        for url in c:
            url = url['url']
            url += '/tsRole/upgrade'
            message = requests.post(url, json.dumps(param))
            message = json.loads(message.text)
            if isinstance(message, dict):
                if message["status"]:
                    raise Exception(message['message'])
                else:
                    sqlstr = "UPDATE ts_role SET tag='%s', branch='%s', create_time='%s', resource_id='%s' WHERE id=%s" % (data['tag'], data['branch'], time, message['message'],data['ts_roleId'])
                    s, f = db.mod(sqlstr)
                    if s:
                        raise Exception("update ts_role failed")
                    ret['message'] = message['message']
            else:
                raise Exception("return value error")
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = 10
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret