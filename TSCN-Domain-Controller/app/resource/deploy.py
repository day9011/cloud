#!/usr/bin/env python2.7
#coding=utf-8
# Name: deploy
# Function: deploy specify service
# Date: 2016-06-12
# Email: day9011@gmail.com
__author__ = 'day9011'

import logging, json
from flask import make_response
from flask import request
from app import domain_controller, services
from utils.auth import get as auth_get
from utils.post_valid import *

logger = logging.getLogger(__name__)
func_list = {
    'FsDriver': services.FsDriver
}

driver = auth_get('compute_driver')
proxy = func_list.get(driver)

@domain_controller.route('/tsRole/deploy', methods=['POST'])
def deploy():
    s = 0
    c = ''
    try:
        arguments = [
            Arg('download_url', required=True, help='Miss download url'),
            Arg('app_name', required=True, help='Miss app name'),
            Arg('config_path', required=False, help='Miss app path'),
            Arg('code_file', required=True, help='Miss file name'),
            Arg('config_url',  required=True, help='Miss config url'),
            Arg('config_name', required=True, help='Miss config name'),
            Arg('build_type', required=True, help='Miss build type'),
            Arg('env', required=False, default=''),
            Arg('version_url', required=False, default=None),
            Arg('restart', required=False, default='False'),
            Arg('exclude', required=False, default=''),
        ]
        s, args = DataIsValid(arguments, request)
        if s:
            c = str(args)
            raise Exception(c)
        print args
        build_type = args['build_type']
        exclude_list = args['exclude']
        config_path = args['config_path']
        config_name = args['config_name']
        app_name = args['app_name']
        code_file = args['code_file']
        download_url = args['download_url']
        config_url = args['config_url']
        env = args['env']
        version_url = args['version_url']
        restart = args['restart']
    except Exception, e:
        logger.error(str(e))
    finally:
        resp = make_response(json.dumps({'status': s, 'message': c}))
        resp.headers['Content-Type']='text/json'
        return resp