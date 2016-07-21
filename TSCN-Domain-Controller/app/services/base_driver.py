#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 25/5/16 PM11:52
# Copyright: TradeShift.com
__author__ = 'liming'

from utils.redis_proxy import redis_proxy
import json
from utils.auth import get as auth_get

cache = redis_proxy()

class Base(object):

    def __init__(self, ts_resourceId):

        self.ts_roleName = None
        self.ts_resourceId = ts_resourceId
        self.ts_rolePrivIp = None
        self.ts_rolePubIp = None
        self.ts_roleStatus = None
        self.ts_roleUptime = None
        self.ts_roleCpuIdle = None
        self.ts_roleMemIdle = None
        self.ts_roleDiskIdle = None
        self.ts_roleOwnerHost = None
        self.ts_rolePort = None
        self.ts_roleCpu = None
        self.ts_roleMem = None
        self.ts_roleDisk = None

    def _get_hardware(self):
        # # d = cache.get_dict('resource_' + self.ts_resourceId)
        # # self.ts_roleName = d.get('RoleName')
        # # self.ts_roleOwnerHost = d.get('OwnerHost')
        # # self.ts_rolePrivIp = d.get('PrivIp')
        # # self.ts_rolePubIp = d.get('PubIp')
        # # self.ts_roleCpu = d.get('Cpu')
        # # self.ts_roleMem = d.get('Mem')
        # # self.ts_roleDisk = d.get('Disk')
        # # self.ts_rolePort = d.get('Port')
        # d = self.ts_resourceId.split('[ts-cloud]')
        # if len(d) == 2:
        #     self.ts_roleOwnerHost = d[0]
        #     self.ts_roleName = d[1]
        #
        # return self.ts_roleOwnerHost
        return None

    def pre_action(self, action):
        if action == 'start':
            new = 'starting'
        elif action == 'stop':
            new = 'stopping'
        elif action == 'restart':
            new = 'restarting'
        elif action == 'upgrade':
            new = 'upgrading'
        else:
            new = 'unknown'

        ori_status = cache.get('status_' + self.ts_roleName)
        if not ori_status:
            # if has no status, make a new one for preventing new action coming
            ori = {}
        else:
            ori = json.loads(ori_status)

        ori.update({'status': new})

        cache.set('status_' + self.ts_roleName, json.dumps(ori), ttl=auth_get('status_ttl'))

    def post_action(self, new_status):
        ori_status = cache.get('status_' + self.ts_roleName)
        if not ori_status:
            # if has no status, make a new one for preventing new action coming
            ori = {}
        else:
            ori = json.loads(ori_status)

        ori.update({'status': new_status})

        cache.set('status_' + self.ts_roleName, json.dumps(ori), ttl=auth_get('status_ttl'))

    def action(self, action):
        pass

    def collect(self):
        pass

    def basic(self):
        # get basic resource info
        pass

    def status(self):
        pass

    def create(self, **kwargs):
        pass
    # def cron_update(self, all_data):
    #
    #     for each_app in all_data:
    #         # status content
    #         k = each_app['resource_id']
    #         v = {'status': each_app['status'],
    #              'uptime': each_app['uptime'],
    #              'cpu_idle': each_app['cpu_idle'],
    #              'mem_idle': each_app['mem_idle'],
    #              'disk_idle': each_app['disk_idle'],
    #              'priv_ip': each_app['priv_ip'],
    #              'pub_ip': each_app['pub_ip'],
    #              }
    #         cache.set('status_' + k, json.dumps(v), ttl=auth_get('status_ttl'))
    #     # detail content

    def delete(self, backup=False, **kwargs):
        pass
