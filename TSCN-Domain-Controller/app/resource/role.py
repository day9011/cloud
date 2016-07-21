#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 25/5/16 PM10:52
# Copyright: TradeShift.com
__author__ = 'liming'

import logging, json
from flask import make_response
from app import domain_controller, services
from utils.auth import get as auth_get
from flask import request

logger = logging.getLogger(__name__)
func_list = {
    'FsDriver': services.FsDriver,
    'Docker': services.DockerDriver
}

driver = auth_get('compute_driver')
proxy = func_list.get(driver)

@domain_controller.route('/tsRole/<string:ts_resourceId>/<string:action>', methods=['POST'])
def tsRoleAction(ts_resourceId, action):
    if proxy is None:
        logger.error('Driver undefined: %s' % driver)
        s, c = 9, 'Internal Error'
    else:
        s, c = proxy(ts_resourceId).action(action)
    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp

@domain_controller.route('/tsRole/status/<string:ts_resourceId>', methods=['GET'])
def tsRoleStatus(ts_resourceId):
    s = 0
    if proxy is None:
        logger.error('Driver undefined: %s' % driver)
        s, c = 9, 'Internal Error'
    else:
        c = proxy(ts_resourceId).status

    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp

@domain_controller.route('/tsRole/collect', methods=['POST'])
def tsCollect():
    logger.info("collect")
    if proxy is None:
        logger.error('Driver undefined: %s' % driver)
        s, c = 9, 'Internal Error'
    else:
        c = proxy(None).collect()
        s = 0
    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp

@domain_controller.route('/tsRole/create', methods=['POST'])
def tsCreateRole():

    if proxy is None:
        logger.error('Driver undefined: %s' % driver)
        s, c = 9, 'Internal Error'
    else:
        if driver == 'FsDriver':
            s, c = 8, 'Not Support'
        else:
            create_value = ''
            tsRoleName, roleName, cpu, mem, image, port, env = None, None, None, None, None, None, None
            try:
                s, c = 0, ''
                create_value = request.form.get('create_value')
                v = json.loads(create_value)
                tsRoleName = v['tsRoleName']
                roleName = v['roleName']
                cpu = v['cpu']
                mem = v['mem']
                image = v['image']
                port = v['port']
                env = v['env']
                if not isinstance(port, list):
                    logger.debug('Port format error: %s' % port)
                    s, c = 1, 'Port format error'
                if not isinstance(env, dict):
                    logger.debug('env format error: %s' % env)
                    s, c = 1, 'Env format error'

            except Exception, e:
                logger.error('Create para parser error: %s, %s' %(create_value, str(e)))
                s, c = 2, 'Bad Options'

            if not s:
                s, c = proxy(None).create(tsRoleName, roleName, cpu, mem, image, port, env, num=1, disk=None)

    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type'] = 'text/json'
    return resp

@domain_controller.route('/tsRole/delete', methods=['POST'])
def tsDeleteRole():
    tsResourceId = request.form.get('tsResourceId', None)
    if tsResourceId is None:
        s, c = 8, 'Miss resource id'
    else:
        if proxy is None:
            logger.error('Driver undefined: %s' % driver)
            s, c = 9, 'Internal Error'
        else:
            s, c = proxy(tsResourceId).delete()
    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp

@domain_controller.route('/tsRole/upgrade', methods=['POST'])
def tsUpgradeRole():
    data = json.loads(request.get_data())
    print data
    tsResourceId = data['tsResourceId']
    if tsResourceId is None:
        s, c = 8, 'Miss resource id'
    else:
        if proxy is None:
            logger.error('Driver undefined: %s' % driver)
            s, c = 9, 'Internal Error'
        else:
            s, c = proxy(tsResourceId).delete()
            if s==0 :
                if driver == 'FsDriver':
                    s, c = 8, 'Not Support'
                else:
                    tsRoleName, roleName, cpu, mem, image, port, env = None, None, None, None, None, None, None
                    try:
                        s, c = 0, ''
                        v = data['create_value']
                        print 'create_value:',v
                        tsRoleName = v['tsRoleName']
                        roleName = v['roleName']
                        cpu = v['cpu']
                        mem = v['mem']
                        image = v['image']
                        port = v['port']
                        env = v['env']
                        if not isinstance(port, list):
                            logger.debug('Port format error: %s' % port)
                            s, c = 1, 'Port format error'
                        if not isinstance(env, dict):
                            logger.debug('env format error: %s' % env)
                            s, c = 1, 'Env format error'

                    except Exception, e:
                        logger.error('Create para parser error: %s, %s' %(v, str(e)))
                        s, c = 2, 'Bad Options'

                    if not s:
                        s, c = proxy(None).create(tsRoleName, roleName, cpu, mem, image, port, env, num=1, disk=None)

    resp = make_response(json.dumps({'status': s, 'message': c}))
    resp.headers['Content-Type']='text/json'
    return resp