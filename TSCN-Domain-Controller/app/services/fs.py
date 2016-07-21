#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 25/5/16 PM11:29
# Copyright: TradeShift.com
__author__ = 'liming'

import logging
from utils.common import http_call
from utils.auth import get as auth_get
from .base_driver import Base
import yaml
import threading
from utils.common import ActivePool

logger = logging.getLogger(__name__)


class FsDriver(Base):

    def __init__(self, ts_resourceId):
        Base.__init__(self, ts_resourceId)

    def action(self, action):
        logger.info('Receive supervisor action: %s, %s' % (self.ts_resourceId, action))
        Owner = self._get_hardware()
        if Owner is None:
            return 1, 'Resource Not Exist'

        # change status to doing
        # self.pre_action(action)
        url = 'http://%s:%s/app/action/%s/%s' % (Owner, auth_get('agent_port'), self.ts_roleName, action)
        s, c = http_call(url, method='post')

        # change status to latest
        if s:
            new_status = 'unknown'
        else:
            s = c['status']
            new_status = c['content']
        # self.post_action(new_status)

        return s, new_status

    def _get_hardware(self):
        d = self.ts_resourceId.split('[TSCloud]')
        if len(d) == 2:
            self.ts_roleOwnerHost = d[0]
            self.ts_roleName = d[1]

        return self.ts_roleOwnerHost

    def upgrade(self, tag):
        pass

    def collect(self):

        def get_status(server):
            # get each status
            url_template = 'http://{ip}:5005/app/collect'
            url = url_template.format(ip=server)
            try:
                s, c = http_call(url=url, method='post')

                if not s:
                    content = c['content']

                    for i in content:
                        # use server ip as app priv_ip
                        # use server ip + app_name as resource_id
                        i.update({'priv_ip': server,
                                  'port': None,
                                  'resource_id': server + '[TSCloud]' + i['name']})
                    return content
                else:
                    # return nothing
                    return []

            except Exception, e:
                logger.error('fail to get app status: %s : %s' % (server, e.args))
                return []

        def get_app_list():
            with open('conf/nodes.yml') as f:
                return yaml.load(f.read())['nodes']

        pool = ActivePool()
        servers = get_app_list()
        check_thread = auth_get('check_thread')
        semaphore_num = check_thread if len(servers) >= check_thread else 1
        s = threading.Semaphore(semaphore_num)

        app_info = []
        def run_get_info(s, pool, server):
            with s:
                pool.makeActive(server)
                r = get_status(server)
                pool.makeInactive(server)
                if r:
                    for i in r:
                        app_info.append(i)

        threads = []
        for i in servers:
            t = threading.Thread(target=run_get_info, args=((s, pool, i)))
            t.start()
            threads.append(t)

        for j in threads:
            j.join()

        return app_info

    def create(self, **kwargs):
        return 9, 'Not Support'
