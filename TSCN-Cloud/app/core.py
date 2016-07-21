#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 13/5/16 AM12:23
# Copyright: TradeShift.com
__author__ = 'liming'
import json
import logging
import time
import urllib
import uuid

import redis
import requests
import xmltodict
from flask import (request,
                   render_template,
                   make_response,
                   redirect)

from app.services.option import (getRoleId, getDomains)
from . import app
from services.role import (TSRoleList, TSROLE)


pageFlag=''
profilename=''

logger = logging.getLogger(__name__)


from app.auth import get as auth_get


@app.route('/favicon.ico')
def favicon():
    logger.debug("favicon")
    return 'NOT FOUND', 404


@app.errorhandler(500)
def err_internal_error(error):
    logger.exception(error.message)


@app.errorhandler(404)
def err_not_found(error):
    # logger.error(error)
    logger.warning(error)
    return render_template('404.html')

@app.route('/')
def indexPage():
    return render_template('main.html')


@app.route('/logout')
def logout():
    # redirect_to = urllib.quote(auth_get('local'), '')
    redirect_to = auth_get('local')
    return redirect('%s?service=%s' % (auth_get('logout_url'), redirect_to))



@app.route('/login/<string:route>')
def login(route):
    print route
    redirect_to = urllib.quote('{0}/{1}'.format(auth_get('local'), route), '')
    return redirect('%s?service=%s' % (auth_get('auth_url'), redirect_to))


@app.route('/<string:project>/services/<string:service_type>')
def show_ts_service(project, service_type):
    RoleIds = getRoleId(project, service_type)
    Domains = getDomains(project)
    pageFlag = 'show_ts_service'
    profilename = 'admin'
    logger.debug("create PageFlag=" + pageFlag)

    tag_server_url = r"http://" + str(auth_get('tag_server')) + r":" + str(auth_get('tag_port'))
    return render_template('ts_service.html', tag_server_url=tag_server_url, flag=pageFlag, RoleIds=RoleIds, Domains=Domains, username=profilename)

@app.route('/getRoleList/<string:project>/<int:domain_id>/<int:role_id>')
def getRoleList(project, domain_id, role_id):
    # url = 'http://{0}/records/idcs'.format(auth_get('getUserInfo'))
    # url = auth_get('getRoleList')
    # r = requests.get('%s/%s/%s' % (url, domain_id, role_id))
    # if r.status_code != 200:
    #     d = json.dumps({'status': 0, 'message': []})
    # else:
    #     d = r.content
    s, c = TSRoleList(project, domain_id, role_id)

    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp

@app.route('/getRoleDetail/<string:project>/<int:ts_role_id>')
def getRoleDetail(project, ts_role_id):
    # url = 'http://{0}/records/idcs'.format(auth_get('getUserInfo'))
    url = auth_get('getRoleDetail')
    r = requests.get('%s/%s' % (url, ts_role_id))
    if r.status_code != 200:
        d = json.dumps({'status': 0, 'message': {}})
    else:
        d = r.content
    resp = make_response(d)
    resp.headers['Content-Type']='text/json'
    return resp

@app.route('/<string:project>/action/<string:action>', methods=['POST',])
def roleAction(project, action):
    ts_roleId = request.form.get('ts_roleId', None)
    if ts_roleId is None:
        d = {'status': 9, 'message': 'Miss id'}
    else:
        if action.lower() not in ('start', 'stop', 'restart'):
            d = {'status': 9, 'message': 'Invalid Action'}
        else:
            ThisRole = TSROLE(ts_roleId)
            ThisRole._basic()
            if ThisRole.domain_id is None:
                d = {'status': 1, 'message': 'Not Exist'}
            else:
                s, c = ThisRole.action(action.lower())
                d = {'status': s, 'message': c}

    resp = make_response(json.dumps(d))
    resp.headers['Content-Type']='text/json'
    return resp

@app.route('/<string:project>/role/<int:ts_roleId>/status', methods=['GET',])
def roleStatus(project, ts_roleId):
    r = TSROLE(ts_roleId)
    s = r.status
    resp = make_response(json.dumps({'status': 0, 'message': s}))
    resp.headers['Content-Type']='text/json'
    return resp



