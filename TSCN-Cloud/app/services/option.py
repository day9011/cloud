#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 13/5/16 AM12:23
# Copyright: TradeShift.com
__author__ = 'liming'

import json
import uuid
import time
import urllib
import logging

import redis
import xmltodict
import requests
from flask import (request,
                   render_template,
                   make_response,
                   redirect)

from app import app


pageFlag=''
profilename=''

logger = logging.getLogger(__name__)
from app.utils.db import Db_access

db = Db_access()

from app.auth import get as auth_get

def getRoleId(project_name, t):
    # url = auth_get('getServiceTypes')
    # r = requests.get(url + '/' + project_name + '/' + t)
    # if r.status_code != 200:
    #     d = {'status': 0, 'message': []}
    # else:
    #     d = r.content
    s, c = db.get("SELECT a.id as id,a.detail as detail,a.name as name FROM role a INNER JOIN project b ON a.project_id=b.id WHERE b.name='%s'" % project_name)
    if s:
        return []
    else:
        return c

def getDomains(project_name):
    # url = 'http://{0}/records/idcs'.format(auth_get('getUserInfo'))
    # url = auth_get('getDomains')
    # r = requests.get(url + '/' + project_name)
    # if r.status_code != 200:
    #     d = {'status': 0, 'message': []}
    # else:
    #     d = r.content
    s, c = db.get("SELECT a.id as id,a.detail as detail,a.name as name FROM domain a INNER JOIN project b ON a.project_id=b.id WHERE b.name='%s'" % project_name)

    if s:
        return []
    else:
        return c
