# -*- coding:utf-8 -*-
__author__ = 'liming'
import xmlrpclib
from working_thread import ActivePool
import threading
from log import create_logger
from db import Db_access
from redis_proxy import redis_proxy
import socket
import time
from utils.common import http_call

logger = create_logger(__name__)

def _cur_time(t_stamp=None):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_stamp))

def get_rpc_list():
    sql = 'select a.id as app_id, a.name, b.ip, b.user, b.password from app a inner join server b on a.server_id = b.id'

    _, c = Db_access().get(sql)
    return c

def update_status(app_list):
    logger.debug('start to update app_list to cache')
    r = redis_proxy()
    for _app in app_list:
        r.set(_app['id'], _app['status'].lower())
        _start = _app.get('start_time')
        start_time = _cur_time(_start) if _start is not None else 'unknown'
        r.set('start_time_' + str(_app['id']), start_time)
    logger.debug('finish update app_list')


def get_status_old(a_info):
    state = 'unknown'
    start_time = None
    a_id = a_info['app_id']
    url_template = 'http://{user}:{password}@{ip}:9001/RPC2'
    url = url_template.format(user=a_info['user'], password=a_info['password'], ip=a_info['ip'])
    try:
        p = xmlrpclib.Server(url)
        # set rpc time out
        socket.setdefaulttimeout(3)
        s = p.supervisor.getProcessInfo(a_info['name'])
        state = s['statename'].lower()
        start_time = s.get('start')
    except Exception, e:
        logger.error('fail to get app status: %s : %s' % (a_info, e.args))
    finally:
        return {'id': a_id, 'status': state, 'start_time': start_time}

def get_status(a_info):
    state = 'unknown'
    start_time = None
    a_id = a_info['app_id']
    url_template = 'http://{ip}:5005/app/status/{app_name}/all'
    url = url_template.format(ip=a_info['ip'], app_name=a_info['name'])
    try:
        s, c = http_call(url=url, method='post')
        if not s:
            content = c['content']
            if content.get('statename') is not None:
                state = content.get('statename')
            if content.get('start') is not None:
                start_time = content.get('start')

    except Exception, e:
        logger.error('fail to get app status: %s : %s' % (a_info, e.args))
    finally:
        return {'id': a_id, 'status': state, 'start_time': start_time}

def main():
    # app_sql = "select a.name as name, a.id as app_ip, b.ip, b.user, b.password from app a " \
    #           "inner join server b on a.server_id = b.id where b.status = 'online'"
    #
    # _, c = Db_access().get(app_sql)
    # for each_app in c:
    #         args = (each_app['app_id'], each_app['name'], each_app['ip'], each_app['user'], each_app['password'])
    #         pool.append(Thread(target=get_set_status, args=args))
    pool = ActivePool()
    s = threading.Semaphore(3)

    app_info = []
    def run_get_status(s, pool, app):
        with s:
            name = str(app['app_id'])
            pool.makeActive(name)
            r = get_status(app)
            pool.makeInactive(name)
            app_info.append(r)

    threads = []
    for i in get_rpc_list():
        t = threading.Thread(target=run_get_status, args=((s, pool, i)))
        t.start()
        threads.append(t)

    for j in threads:
        j.join()

    update_status(app_info)

