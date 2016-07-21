#!/usr/bin/env python2.7
#coding=utf-8
# Name: upgrade
# Function: upgrade role
# Date: 2016-06-13
# Email: day9011@gmail.com
__author__ = 'day9011'

__all__ = []

from . import app
from app.utils.db import Db_access
from flask import (request,
                   render_template,
                   make_response,
                   redirect)
from services.role import TSROLE, TSRoleList
import json
import logging
from app.utils.redis_proxy import RedisProxy
cache = RedisProxy()
import requests

logger = logging.getLogger(__name__)
db = Db_access()

@app.route('/ts/data/project/list', methods=['GET'])
def get_project_list():
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT * FROM project'
        s, project_list = db.get(sql_str)
        if s:
            raise Exception("get project list error")
        else:
            ret['message'] = project_list
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/role_template/<string:project>/<string:domain_id>/<string:role_id>', methods=['GET'])
def get_role_template(project, domain_id, role_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT cpu, mem, disk FROM project_role WHERE domain_id=%s AND role_id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, role_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get role template error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/role_list/<string:project>/<string:domain_id>', methods=['GET'])
def get_role_list(project, domain_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT id, name FROM role WHERE domain_id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get role list error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/role_detail/<string:project>/<string:domain_id>/<string:role_id>', methods=['GET'])
def get_role_detail(project, domain_id, role_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT port FROM role WHERE domain_id=%s AND id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, role_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get role detail error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/role_seq/<string:project>/<string:domain_id>/<string:role_id>', methods=['GET'])
def get_role_req(project, domain_id, role_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT max(role_seq) as seq FROM ts_role WHERE domain_id=%s AND role_id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, role_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get role seq error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret


@app.route('/ts/data/domain_info/<string:project>/<string:domain_id>', methods=['GET'])
def get_domain_controller_url(project, domain_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT url FROM domain WHERE id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get domain info error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/env/<string:project>/<string:domain_id>/<string:role_id>', methods=['GET'])
def get_env(project, domain_id, role_id):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sql_str = 'SELECT key_name as k, key_value as v FROM var_table WHERE domain_id=%s AND role_id=%s ' \
                  'AND project_id=(SELECT id FROM project WHERE name="%s");' % (domain_id, role_id, project)
        s, temp_dict = db.get(sql_str)
        if s or not temp_dict:
            raise Exception("get env error")
        else:
            ret['message'] = temp_dict
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret

@app.route('/ts/data/tsrole/status/<int:ts_roleId>', methods=['GET'])
def get_ts_role_status(ts_roleId):
    ret = {'status': 0, 'message': 'OK'}
    try:
        sqlstr = 'SELECT resource_id FROM ts_role WHERE id=%d' % (ts_roleId)
        s, temp_dict = db.get(sqlstr)
        if s or not temp_dict:
            raise Exception("get resource id error")
        else:
            resource_id = temp_dict[0]['resource_id']
        s, c = db.get("SELECT url FROM domain WHERE id=(select domain_id from ts_role where id=%s)" % (str(ts_roleId)))
        if s or not c:
            raise Exception('Get domain list fail: %s' % c)
        url = c[0]['url']
        message = requests.get(url + '/tsRole/status/' + resource_id)
        message = json.loads(message.text)
        if isinstance(message, dict):
            if message["status"]:
                raise Exception(message)
            else:
                ret = message
                data = message['message']
                cache.set(data['name'], json.dumps(data))
        else:
            raise Exception("return value error")
    except Exception, e:
        logger.error('Error: %s' % str(e))
        ret['status'] = -100
        ret['message'] = str(e)
    finally:
        print ret
        ret = json.dumps(ret)
        ret = make_response(ret)
        ret.headers['Content-Type']='text/json'
        return ret
