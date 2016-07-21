#!/usr/bin/env python2.7
#coding=utf-8
# Name: create
# Function: create api
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

@app.route('/ts/create/tsRole', methods=['POST'])
def create_tsRole():
    ret = {'status': 0, 'message': 'OK'}
    try:
        data = json.loads(request.get_data())
        sqlstr = "SELECT id as project_id FROM project WHERE name='%s'" % (data['project'])
        s, f = db.get(sqlstr)
        if s:
            raise Exception("query project id error")
        project_id = f[0]['project_id']
        time = get_current()
        image = data['image'] + ':' + data['branch'] + '-' + data['tag']
        param = {
            'seq': data['seq'],
            'tsRoleName': data['tsRoleName'],
            'roleName': data['roleName'],
            'cpu': data['cpu'],
            'mem': data['mem'],
            'image': image,
            'port': data['port'],
            'env': data['env'],
        }
        print param
        s, c = db.get("SELECT url FROM domain WHERE id = %s" % (data['domain']))
        if s or not c:
            raise Exception('Get domain list fail: %s' % c)
        url = c[0]['url']
        sqlstr = "INSERT INTO ts_role VALUES (NULL, '%s', %s, %s, %s, %s, '', %d, '%s', '%s', '%s')" % (
            data['tsRoleName'], project_id, data['domain'], data['role_id'], data['seq'], 1, data['tag'], time, data['branch'])
        print sqlstr
        message = requests.post(url + '/tsRole/create', {'create_value': json.dumps(param)})
        db.mod(sqlstr)
        message = json.loads(message.text)
        if isinstance(message, dict):
            if message["status"]:
                sqlstr = "DELETE FROM ts_role WHERE name='%s'" % (data['tsRoleName'])
                db.mod(sqlstr)
                raise Exception(message['message'])
            else:
                sqlstr = "UPDATE ts_role SET resource_id='%s' WHERE name='%s'" % (message['message'], data['tsRoleName'])
                logger.info(sqlstr)
                db.mod(sqlstr)
                sqlstr = "SELECT id FROM ts_role WHERE name='%s'" % (data['tsRoleName'])
                s, f = db.get(sqlstr)
                if s:
                    raise Exception("query ts_role id error")
                ts_roleId = f[0]['id']
                ret['message'] = ts_roleId
        else:
            raise Exception("return value error")
    except Exception, e:
        try:
            sqlstr = "DELETE FROM ts_role WHERE name='%s'" % (data['tsRoleName'])
            db.mod(sqlstr)
        except:
            pass
        logger.error('Get domain list fail: %s' % str(e))
        ret['status'] = 10
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret