#!/usr/bin/env python2.7
#coding=utf-8
# Name: delete
# Function: delete api
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
import logging

logger = logging.getLogger(__name__)
db = Db_access()

@app.route('/ts/delete/tsRole', methods=['POST'])
def delete_tsRole():
    ret = {'status': 0, 'message': 'OK'}
    try:
        data = json.loads(request.get_data())
        s, c = db.get("SELECT url FROM domain WHERE id=(select domain_id from ts_role where id=%s)" % (data['ts_roleId']))
        if s or not c:
            raise Exception('Get domain list fail: %s' % c)
        url = c[0]['url']
        sqlstr = "SELECT resource_id FROM ts_role WHERE id=%s" % (data['ts_roleId'])
        s, f = db.get(sqlstr)
        if s:
            raise Exception("query containeid id error")
        resource_id = f[0]['resource_id']
        param = {
            'tsResourceId': resource_id,
        }
        message = requests.post(url + '/tsRole/delete', param)
        message = json.loads(message.text)
        if isinstance(message, dict):
            if message["status"]:
                raise Exception(message['message'])
            else:
                sqlstr = "DELETE FROM ts_role WHERE id=%s" % (data['ts_roleId'])
                s, f = db.mod(sqlstr)
                if s:
                    raise Exception("delete ts_role failed")
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