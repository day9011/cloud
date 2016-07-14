#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 1/6/16 PM3:24
# Copyright: TradeShift.com
__author__ = 'liming'

import threading, logging, requests, json
from app.utils.redis_proxy import RedisProxy
from app.utils.db import Db_access
from app.auth import get as auth_get

cache = RedisProxy()
db = Db_access()
logger = logging.getLogger(__name__)


class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):

        with self.lock:
            # print 'start thread %s' % name
            self.active.append(name)

    def makeInactive(self, name):

        with self.lock:
            # print 'stop thread %s' % name
            self.active.remove(name)


def info_collect():

    def get_status(controller):
        # get each status
        url_template = '{ip}/tsRole/collect'
        url = url_template.format(ip=controller)
        print url
        try:
            r = requests.post(url=url, timeout=60)
            if r.status_code != 200:
                print 'Controller return error: %s, %s' %(r.status_code, r.reason)
                logger.error('Controller return error: %s, %s' %(r.status_code, r.reason))
                return []
            else:
                return r.json()['message']

        except Exception, e:
            print 'fail to get app status: %s : %s' % (controller, e.args)
            logger.error('fail to get app status: %s : %s' % (controller, e.args))
            return []

    def update_cache(controller):
        infos = get_status(controller)
        for i in infos:
            d = {'status': i.get('status'),
                 'priv_ip': i.get('priv_ip'),
                 'pub_ip': i.get('pub_ip'),
                 'priv_in': i.get('priv_in'),
                 'priv_out': i.get('priv_out'),
                 'pub_in': i.get('pub_in'),
                 'pub_out': i.get('pub_out'),
                 'stderr_logfile': i.get('stderr_logfile'),
                 'logfile': i.get('logfile'),
                 'port': i.get('port'),
                 'cpu_idle': i.get('cpu_idle'),
                 'mem_idle': i.get('mem_idle'),
                 'disk_idle': i.get('disk_idle'),
                 'uptime': i.get('uptime'),
                 'name': i.get('name'),
                 }
            cache.set(i.get('name'), json.dumps(d), ttl=auth_get('status_ttl'))


    def get_domain():
        s, c = db.get("SELECT url FROM domain")
        if s:
            logger.error('Get domain list fail: %s' % c)
            return []
        else:
            return c

    pool = ActivePool()
    domains = get_domain()
    logger.debug('Get domains: %s' % domains)

    semaphore_num = 5 if len(domains) >= 5 else 1

    s = threading.Semaphore(semaphore_num)

    # app_info = []

    def update_info(s, pool, controller):
        with s:
            pool.makeActive(controller)
            update_cache(controller)
            pool.makeInactive(controller)
            # if r:
            #     for i in r:
            #         app_info.append(i)

    threads = []
    for i in domains:
        controller = i['url']
        if controller:
            t = threading.Thread(target=update_info, args=((s, pool, controller)))
            t.start()
            threads.append(t)

    for j in threads:
        j.join()



