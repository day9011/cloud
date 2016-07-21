#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 26/5/16 PM1:03
# Copyright: TradeShift.com
__author__ = 'liming'
import docker, logging, json, threading
from docker.utils import Ulimit
from utils.common import ActivePool, tztime2datatime
from app.services.base_driver import Base
from utils.auth import get as auth_get
import requests


logger = logging.getLogger(__name__)

def translate_status(status):
    _status = {
        'exited': 'stopped',
        'stopped': 'stopped',
        'running': 'running',
        'paused': 'stopped',
        'crashed': 'critical',
        None: 'unknown',
        '': 'unknown'
    }

    s = _status.get(status.lower(), None)
    if s:
        return s
    else:
        return 'unknown'

class DockerDriver(Base):

    def __init__(self, ts_resourceId):
        Base.__init__(self, ts_resourceId)
        self.cli = docker.Client(base_url=auth_get('docker_api'), timeout=60)

    def action(self, action):
        logger.info('Receive docker action: %s, %s' % (self.ts_resourceId, action))
        actions = {
            'start': self.cli.start,
            'stop': self.cli.stop,
            'restart': self.cli.restart
        }
        ori_status = 'unknown'
        # try:
        #     ori_status = self.basic()['status']
        #     fun = actions[action]
        #     fun(resource_id=self.ts_resourceId)
        #     new_status = self.get_status(self.cli, self.ts_resourceId, need_stat=False)['status']
        #     return 0, translate_status(new_status)
        # except Exception, e:
        #     logger.error('Action failed: %s' % str(e))
        #     return 1, translate_status(ori_status)

        ori_status = self.get_status(self.cli, self.ts_resourceId, need_stat=False)['status']
        fun = actions[action]
        fun(resource_id=self.ts_resourceId)
        new_status = self.get_status(self.cli, self.ts_resourceId, need_stat=False)['status']
        print self.get_status(self.cli, self.ts_resourceId, need_stat=False)['status']
        return 0, translate_status(new_status)

    @staticmethod
    def get_status(docker_api, resource_id=None, need_stat=False):

        def _inspect_container(docker_api, resource_id):
            try:
                info = docker_api.inspect_container(resource_id=resource_id)
            except Exception, e:
                logger.error('Get container basic error: %s, %s' % (resource_id, str(e.args)))
                info = {}
            return info

        def basic(docker_api, resource_id):
            info = _inspect_container(docker_api, resource_id)
            if not info:
                return info
            ts_roleName = info['Name'].strip('/')
            owner = info['Node']['IP']
            # owner = "172.16.30.180"
            cpu_share = info['HostConfig']['CpuShares']
            host_cpu = info['Node']['Cpus']
            # host_cpu = 1
            cpu = host_cpu * cpu_share / 1024
            mem = info['HostConfig']['Memory']
            disk = None
            priv_ip = owner
            ports = info['HostConfig']['PortBindings']
            _s = info['State']
            error = _s['Error']
            status = translate_status(_s['Status'])
            uptime = tztime2datatime(_s['StartedAt'])
            # _image = info['Image']
            # _tag = self.cli.inspect_image(resource_id=_image)['RepoTags']
            _tag = info['Config']['Image']
            # some tags from docker-py looks like 192.168.100.2:5000/nginx:latest
            tag = _tag.split('/')[-1]
            index = tag.find(':')
            if index != -1:
                tag = tag[index + 1:]
            info = {
                'status': status,
                'uptime': uptime,
                'logfile': '',
                'stdout_logfile': '',
                'stderr_logfile': '',
                'name': ts_roleName,
                'priv_ip': priv_ip,
                'pub_ip': None,
                'tag': tag,
                'owner': owner,
                'cpu': cpu,
                'mem': mem,
                'disk': disk,
                'error': error,
                'port': ports
            }
            return info

        def stat(docker_api, resource_id):
            info = {}
            try:
                stat = docker_api.stats(resource_id=resource_id, decode=None, stream=True)
                pre = json.loads(stat.next())
                latest = json.loads(stat.next())
                cpu_total_usage = latest['cpu_stats']['cpu_usage']['total_usage'] - pre['cpu_stats']['cpu_usage']['total_usage']
                cpu_system_uasge = latest['cpu_stats']['system_cpu_usage'] - pre['cpu_stats']['system_cpu_usage']
                cpu_num = len(pre['cpu_stats']['cpu_usage']['percpu_usage'])
                cpu_usage = round((float(cpu_total_usage)/float(cpu_system_uasge)) * cpu_num * 100.0, 2)
                mem_now_usage = latest['memory_stats']['usage']
                mem_limit = latest['memory_stats']['limit']
                mem_usage = round(float(mem_now_usage)/float(mem_limit) * 100.0, 2)
                # todo: network traffic
                priv_out = None
                priv_in = None
                pub_out = None
                pub_in = None
                disk_idle = round(100, 2)
                cpu_idle = round(100 - cpu_usage, 2)
                mem_idle = round(100 - mem_usage, 2)


                info = {
                    'cpu_idle': cpu_idle,
                    'mem_idle': mem_idle,
                    'disk_idle': disk_idle,
                    'priv_in': priv_in,
                    'pub_in': pub_in,
                    'priv_out': priv_out,
                    'pub_out': pub_out
                }
            except:
                pass
            finally:
                return info

        if resource_id is None:
            return {}

        content = basic(docker_api, resource_id)
        if need_stat is True:
            content.update(stat(docker_api, resource_id))

        return content

    def collect(self):

        docker_api = docker.Client(base_url=auth_get('docker_api'), timeout=5)
        get_status = self.get_status

        def get_app_list():
            li = []
            for each_app in docker_api.containers(all=True):
                if 'bwts-registrator' in each_app['Names'][0]:
                    # registrator app for consul
                    continue
                li.append(each_app['Id'])

            return li

        pool = ActivePool()
        containers = get_app_list()
        check_thread = auth_get('check_thread')
        semaphore_num = check_thread if len(containers) >= check_thread else 1
        s = threading.Semaphore(semaphore_num)

        app_info = []
        def run_get_info(s, pool, docker_api, container):
            try:
                with s:
                    pool.makeActive(container)
                    r = get_status(docker_api, container, need_stat=True)
                    pool.makeInactive(container)
                    if r:
                        app_info.append(r)
            except:
                pass


        threads = []
        for i in containers:
            t = threading.Thread(target=run_get_info, args=((s, pool, docker_api, i.strip())))
            t.start()
            threads.append(t)

        for j in threads:
            j.join()

        logger.info("Get info successfully")
        return app_info

    @property
    def status(self):
        return self.get_status(self.cli, self.ts_resourceId, need_stat=True)

    def create(self, tsRoleName, roleName, cpu, mem, image, port, env, num=1, disk=None):
        # example:
        # seq = 9
        # d = {
        # 'seq' : seq,
        # 'tsRoleName' : 'web%s.bwts.ct.com' % seq,
        # 'roleName' : 'lmapp',
        # 'cpu' : 1,
        # 'mem' : int(0.5 * 1024 * 1024 * 1024),
        # 'image' : '192.168.100.2:5000/testweb:new',
        # 'port' : [80],
        # 'env' : {
        # 'name': 'liming',
        # 'age': 30,
        # },
        # }
        # r = requests.post(url + uri, {'create_value': json.dumps(d)})

        logger.info('Receive docker create: %s; %s; %s; %s; %s; %s; %s; %s; %s' % (tsRoleName, roleName, cpu, mem, image, port, env, num, disk))
        if self.ts_resourceId:
            # not a clean instance
            return 9, 'Not Allowed'

        # for consul-template
        env.update({
            'SERVICE_NAME': roleName,
            'SERVICE_ID': tsRoleName,
        })

        # # host_config
        # ulimits = [Ulimit(name='nofile', Hard=65535, Soft=65535)]
        # mem_limit = '512M'
        # dns = ['192.168.100.2',]
        # dns_search = ['bwts.com.ct1',]
        # oom_kill_disable = False
        port_binds = {}
        for each_port in port:
            if not each_port:
                continue
            if not isinstance(each_port, int):
                each_port = int(each_port)

            port_binds.update({each_port: ('0.0.0.0',)})
        _host_config = {
        'ulimits': [Ulimit(name='nofile', Hard=65535, Soft=65535)],
        'mem_limit': mem,
        # 'dns': ['192.168.100.2',],
        'port_bindings': port_binds,
        'restart_policy': {
                            "MaximumRetryCount": 5,
                            "Name": "always"
                            },
        'oom_kill_disable': False
        }

        # host_config = c.create_host_config(ulimits=ulimits, mem_limit='512m', dns=dns, dns_search=dns_search, oom_kill_disable=oom_kill_disable)
        host_config = self.cli.create_host_config(**_host_config)

        para = {
        'image': image,
        'hostname': tsRoleName,
        'detach': True,
        # 'command': 'echo "This is web $SERVICE_ID" > /opt/front/index.html && nginx -g \'daemon off\'',
        'environment': env,
        'name': tsRoleName,
        'cpu_shares': cpu,
        'host_config': host_config
        }
        try:
            container_id = self.cli.create_container(**para)
            if not container_id:
                logger.error('Create container error')
                return 9, 'Create container error'

        except Exception, e:
            logger.error('Create container error: %s' % str(e))
            return 1, str(e)

        try:
            container_id = container_id['Id']
            self.cli.start(resource_id=container_id)
            logger.info('Docker created, id is %s' % container_id)

        except Exception, e:
            logger.error('Start container error: %s' % str(e))
        finally:
            return 0, container_id

    def delete(self, v=False, link=False, backup=False):
        # can not delete a running container
        # example
        # uri = '/tsRole/delete'
        # d = {'rsResourceId': rid}
        # r = requests.post(url + uri, d)

        logger.info('Receive delete: %s' % self.ts_resourceId)
        if not self.ts_resourceId:
            return 9, 'No Target'

        # can not delete a running app
        info = self.get_status(self.cli, resource_id=self.ts_resourceId, need_stat=False)
        if not info:
            logger.debug('Container info is not found: %s' % self.ts_resourceId)
            return 2, 'No app info'
        cur_status = info['status']
        if cur_status == 'running':
            logger.warning('Can not delete a running app: %s' % self.ts_resourceId)
            return 8, 'Can not delete a running app'

        try:
            self.cli.remove_container(resource_id=self.ts_resourceId, force=False, v=False, link=False)
            return 0, 'Done'
        except Exception,e:
            logger.error('Error when delete %s: %s' % (self.ts_resourceId, str(e)))
            return 1, 'Error when delete'






