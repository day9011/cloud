#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 24/5/16 PM1:02
# Copyright: TradeShift.com
__author__ = 'liming'

import logging, json, threading, requests
from app.utils.db import Db_access
from app.utils.redis_proxy import RedisProxy
from app.utils.common import retry
from app.auth import get as auth_get

db = Db_access()
cache = RedisProxy()

logger = logging.getLogger(__name__)

class TSROLE(object):

    def __init__(self, ts_roleId):
        self.role_name = None
        self.role_id = None
        self.code_file = None
        self.config_file = None
        self.config_path = None
        self.build_type = None
        self.type = None
        self.project_id = None
        self.domain_id = None
        self.resource_id = None
        self.port = None
        self.password = None
        self.db_name = None
        self.username = None
        self.private_ip = None
        self.public_ip = None
        self.seq = None
        self.is_enable = None
        self.cpu = None
        self.mem = None
        self.disk = None
        self.create_time = None
        self.controller = None
        self.action_list = {'start': 'starting',
                            'stop': 'stopping',
                            'restart': 'restarting',
                            'upgrade': 'upgrading'}
        self.id = ts_roleId
        self._basic()

    def _basic(self):
        s, c = db.get('SELECT domain_id,project_id,role_id,name,resource_id FROM ts_role WHERE id=%s' % self.id)
        if not s:
            self.domain_id = c[0]['domain_id']
            self.project_id = c[0]['project_id']
            self.role_id = c[0]['role_id']
            self.name = c[0]['name']
            self.resource_id = c[0]['resource_id']

    @property
    def status(self):
        s = cache.get(self.name)
        if s is None:
            return {'status': 'unknown'}
        return s

    def set_status(self, status):
        _status = cache.get(self.name)
        if _status is None:
            return
        new = json.loads(_status)
        new.update({'status': status})

        cache.set(self.name, json.dumps(new), ttl=auth_get('status_ttl'))

    def _get_controller(self):
        self._basic()
        s, c = db.get('SELECT url FROM domain WHERE id=%s' % self.domain_id)
        if not s:
            self.controller = c[0]['url']

    def action(self, action):
        self._get_controller()
        if not self.controller:
            return 2, 'No Controller'
        # change status
        self.set_status(self.action_list[action])
        url = self.controller + '/tsRole/' + self.resource_id + '/' + action

        # update current status
        s, new_status = self._call_controller(url)
        self.set_status(new_status)
        return s, new_status

    @retry(attempt=3)
    def _call_controller(self, url, data=None):
        r = requests.post(url, data)
        if r.status_code != 200:
            return 1, 'HTTP ERROR'
        else:
            return r.json().get('status'), r.json().get('message')


def TSRoleList(project_name, domain_id, role_id):
    s, c = db.get("SELECT id FROM project WHERE name='%s'" % project_name)
    if s or not c:
        return 9, 'No such project %s' % project_name
    else:
        project_id = c[0]['id']

    _sql = """SELECT a.id,a.name,a.tag, a.branch, a.resource_id, a.role_id FROM ts_role a WHERE a.project_id={0} AND a.domain_id={1}"""

    if role_id != 0:
        _sql += " AND a.role_id={2}"

    # add status to info
    s, c = db.get(_sql.format(project_id, domain_id, role_id))
    if not s:
        for i in c:
            # get status from redis
            k = i['name']
            tag = i['branch'] + '-' + i['tag']
            _status = cache.get(k)
            if _status:
                _s = json.loads(_status)
                uptime = _s.get('uptime')
                cpu = _s.get('cpu_idle')
                mem = _s.get('mem_idle')
                status = _s.get('status')
                disk = _s.get('disk_idle')
                priv_ip = _s.get('priv_ip')
                pub_ip = _s.get('pub_ip')
            else:
                uptime = None
                cpu = None
                mem = None
                status = None
                disk = None
                priv_ip = None
                pub_ip = None

            i.update({'status': status,
                      "uptime": uptime,
                      "cpu_idle": cpu,
                      'mem_idle': mem,
                      "disk_idle": disk,
                      "priv_ip": priv_ip,
                      "pub_ip": pub_ip,
                      "tag": tag,
                      })

    return s, c


