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

@app.route('/gcloud')
def index():
    pageFlag = 'vm_create'
    logger.debug("index PageFlag="+pageFlag)
    idcs = getDomains()

    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/gcloud'.format(auth_get("local"))),
            ('ticket', ticket),
        ]
        url = 'https://sso.qiyi.com/cas/serviceValidate?{0}'.format(urllib.urlencode(params))
        print 'request => ', url

        try:
            #r = urllib.urlopen(url)
            r = requests.get(url)

            if 'cas:authenticationSuccess' in r.content:
                username = xmltodict.parse(r.content)['cas:serviceResponse']['cas:authenticationSuccess']['cas:user']
            else:
                username = ''
            
            resp = redirect('/gcloud')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('ts_service.html', flag=pageFlag, idcs=idcs, username=profilename)


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

@app.route('/getRoleDetail/e-invoice/<int:ts_role_id>')
def getRoleDetail(ts_role_id):
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

@app.route('/e-invoice/action/<string:action>', methods=['POST',])
def roleAction(action):
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

@app.route('/e-invoice/role/<int:ts_roleId>/status', methods=['GET',])
def roleStatus(ts_roleId):
    r = TSROLE(ts_roleId)
    s = r.status
    resp = make_response(json.dumps({'status': 0, 'message': s}))
    resp.headers['Content-Type']='text/json'
    return resp

def request_new_ip(cluster_id):
    # url = 'http://{0}/ip'.format(auth_get('get_public_ip'))
    url = auth_get('get_public_ip')
    print url
    r = requests.get(url, data={'cluster_id': cluster_id})
    if r.ok:
        result = r.json()
        if result['status']:
            return None
        else:
            return result['content']
    else:
        return None


def release_ip(ip):
    # url = '{0}/ip/{1}'.format(auth_get('get_public_ip'),ip)

    url = '{0}/{1}'.format(auth_get('get_public_ip'),ip)
    r = requests.delete(url)
    if r.ok:
        result = r.json()
        if result['status']:
            return False
        else:
            return True
    else:
        return False

@app.route('/vm/create/createfunc',methods=['POST'])
def create_vm_func():
    idc_name = request.form.get('idc')
    cluster_name = request.form.get('cluster')
    cluster_id = request.form.get('cluster_id')
    image_name = request.form.get('image_name')
    flavor_name = request.form.get('flavor_name')
    image_id = request.form.get('image_id')
    flavor_id = request.form.get('flavor_id')
    user = request.form.get('user')
    # hostname = request.form.get('hostname')
    need_pub = int(request.form.get('need_pub', 0))
    key_content = request.form.get('key_content')
    key_name = request.form.get('key_name')
    router_path = '/etc/sysconfig/network-scripts/route-eth0'
    osName = request.form.get('osName')


    logger.info('arguments: %s' % request.form.items())

    # DXT_7_cluster1_private_abcded_20160223.201256
    ip_tag = 'public' if need_pub else 'private'
    cur = time.strftime('%Y%m%d.%H%M%S')
    # vm_name = '_'.join([idc_name, cluster_name, ip_tag, uuid.uuid4().hex[:7], cur])
    vm_name = '_'.join([idc_name, cluster_name, uuid.uuid4().hex[:7]])
    create_time = time.strftime('%Y-%m-%d %H:%M:%S')
    if osName == 'linux':
        values = {
            'image_id': image_name,
            'flavor_id': flavor_name,
            'cluster_id': cluster_id,
            'user': user,
            'vm_name': vm_name,
            'key_name': key_name,
            'key_content': key_content,
            'router_path': router_path,
            'create_time': create_time,
        }
    else:
        values = {
            'image_id': image_name,
            'flavor_id': flavor_name,
            'cluster_id': cluster_id,
            'user': user,
            'vm_name': vm_name,
            'key_name': key_name,
            'key_content': key_content,
            'create_time': create_time,
            #'router_path': 'Users\\123.txt',
        }
    print(values)
    # if hostname:
    #     values['hostname'] = hostname

    # TODO: need new public_ip interface.
    if need_pub:
        print("need public ip")
        print  cluster_id
        new_ip = request_new_ip(cluster_id)
        print new_ip
        if new_ip is None:
            return

        ip_info = new_ip
        values.update(public_ip=ip_info['ip'], netmask=ip_info['netmask'], gateway=ip_info['gateway'])
        print values
    else:
        ip_info = None

    # url='http://{0}/vm/create'.format(auth_get('vm_create'))
    url = auth_get('vm_create')
    r = requests.post(url, data=values)
    print("r======= %s" % r)
    print(values)

    if r.ok:
        ret = r.json()
        logger.info(ret)
        instance_id = ret['result']['instance_id']
        # query detail
        print(instance_id)
        #_query_vm_detail('test','cluster1', instance_id)
        userinfo = getUserInfo()
        userid = userinfo.pop('message')[0]['id']
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        createVmData={
            'instance_id': instance_id,
            'idc': idc_name,
            'cluster': cluster_name,
            'cluster_id': cluster_id,
            'vm_name': vm_name,
            'image_id': image_id,
            'flavor_id': flavor_id,
            'user_id': userid,
            'public_ip': ip_info['ip'] if ip_info else '',
            'key_name': key_name,
            'key_content': key_content,
            'create_time': create_time,
        }
        
        CreatestoreInDB(createVmData)
        _query_vm_detail(cluster_id, instance_id)
        logger.debug('createVmData=== %s' % createVmData)
        result = r.json()
        result['result'].update(create_time=create_time)
        logger.debug(result)
        result = json.dumps(result)

    else:
        print "create vm failed"
        # release IP
        print('ip_info %s' % ip_info)
        if ip_info is not None:
            release_ip(ip_info['ip'])
        # reply(ajax)
        result = r.content
        print("result=== %s" % result)
        return make_response(404, {"error": "create vm failed"})

    return make_response(result)


@app.route('/vm/create/StoreCreateData',methods=['POST'])
def CreatestoreInDB(values):
    logger.debug("values %s" % values)
    # url ='http://{0}/instances/records'.format(auth_get('createvm_storeInDB'))
    url = auth_get('StoreCreateData')
    r = requests.post(url,data=values)
    if not r.ok:
        logger.error(r.content)
    resp = make_response(r.content)
    logger.debug("store in DB %s" % resp)
    return resp


@app.route('/vm/startjob',methods=['POST'])
def startjob(values):
    # url = 'http://{0}/instances/records/start'.format(auth_get('createvm_storeInDB'))
    url = auth_get('startjob')
    r = requests.post(url, data=values)
    resp = make_response(r.content)
    return resp


@app.route('/vm/stopjob', methods=['POST'])
def stopjob(values):
    # url = 'http://{0}/instances/records/stop'.format(auth_get('createvm_storeInDB'))
    url = auth_get('stopjob')
    r = requests.post(url,data=values)
    resp = make_response(r.content)
    return resp

@app.route('/vm/deletejob',methods=['POST'])
def deletejob(values):
    # url = 'http://{0}/instances/records/delete'.format(auth_get('createvm_storeInDB'))
    print('begin delete job!')
    url = auth_get('deletejob')
    r = requests.post(url, data=values)
    resp = make_response(r.content)
    print('end delete job!')
    return resp


def _query_vm_detail(cluster_id, instance_id):
    # url='http://{0}/query'.format(auth_get('vm_query_detail'))

    url = '{0}/{1}'.format(auth_get('vm_query_detail'),instance_id)
    values = {
        'cluster_id': cluster_id,
    }

    #url = auth_get('vm_query_detail')

    #values = {
    #    'cluster_id': cluster_id,
    #    'instance_id': instance_id,
    #}
    print("values========== %s" % values)
    r = requests.get(url, params=values)
    print("r====== %s" % r.content)
    return r.content


@app.route('/vm/queryDetail', methods=['GET'])
def query_vm_detail():
    params = dict(request.args)

    cluster_id = params['cluster_id'][0]
    instance_id = params['instance_id'][0]

    result = _query_vm_detail(cluster_id, instance_id)
    print(result)

    resp = make_response(result)
    resp.headers['Content-Type']='text/json'
    return resp


@app.route('/vm/deleteVm', methods=['POST'])
def delete_vm_func():
    print "begin deleteVm"
    cluster_id = request.form.get('cluster_id')
    instance_id = request.form.get('instance_id')
    print "cluster_id:", cluster_id
    #cluster_id = params['cluster_id'][0]
    #instance_id = params['instance_id'][0]

    # DELETE  http://localhost:8009/vm/{cluster_id}/{instance_id}
    # url='http://{0}/vm/{1}/{2}'.format(auth_get('vm_delete_func'), cluster_id, instance_id)
    url = auth_get('deleteVm')
    print("delete url==="+url)

    values = {
        'cluster_id': cluster_id,
        'instance_id': instance_id
    }
    r = requests.post(url,data=values)
    # TODO: delete status
    if r.ok:
        getPubIpresult = _query_vm_detail(cluster_id, instance_id)
        tmp = json.loads(getPubIpresult)
        public_ip = tmp.get('floating_ip')
        deletejob(values)
        logger.debug(public_ip)
        if public_ip:
            release_ip(public_ip)
    resp = make_response(r.content)
    print(r.content)
    resp.headers['Content-Type']='text/json'
    return resp


@app.route('/vm/startVm', methods=['POST'])
def start_vm_func():
    cluster_id = request.form.get('cluster_id')
    instance_id = request.form.get('instance_id')
    # url='http://{0}/vm/start'.format(auth_get('vm_start_func'))
    url = auth_get('startVm')

    values = {
        'instance_id': instance_id,
        'cluster_id': cluster_id,
    }
    startjob(values)
    print(values)
    r = requests.post(url, data=values)
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    print("stop vm %s" % resp)
    return resp


@app.route('/vm/stopVm', methods=['POST'])
def stop_vm_func():
    cluster_id = request.form.get('cluster_id')
    instance_id = request.form.get('instance_id')
    # url='http://{0}/vm/stop'.format(auth_get('vm_stop_func'))
    url = auth_get('stopVm')

    values = {
        'instance_id': instance_id,
        'cluster_id': cluster_id,
    }
    stopjob(values)
    r = requests.post(url, data=values)
    print('stop vm data %s' % values)
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    print("stop vm %s" % resp)
    return resp


@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    # url = 'http://{0}/records/users/{1}'.format(auth_get('getUserInfo'),'admin')
    url = '{0}/{1}'.format(auth_get('getUserInfo'),'admin')
    r = requests.get(url)
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    return r.json()


@app.route('/authoration', methods=['GET'])
def author():
    print 123
    username, passwd ='admin', 'admin'
    params = dict(request.args)
    getUserName = params['username'][0]
    getPassWd = params['passwd'][0]
    logger.debug('username='+getUserName+',password='+getPassWd)
    if (getUserName == username and getPassWd == passwd):
        pageFlag='vm_create'
        profilename = getUserName
        return '0'
    else:
        return '1'

@app.route('/getFlavor/<string:clu_id>', methods=['GET'])
def getFlavor(clu_id):
    # url = 'http://{0}/records/flavors/{1}'.format(auth_get('getUserInfo'),clu_id)

    # url = auth_get('getFlavor')
    # data = {"cluster_id": clu_id}
    # r = requests.get(url,data)

    url = '{0}/{1}'.format(auth_get('getFlavor'),clu_id)
    print(url)
    r = requests.get(url)
    #resp = r.json().pop('message')
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    return resp

@app.route('/getFlavor', methods=['GET'])
def getFlavorList():
    url = auth_get('getFlavor')
    print(url)
    r = requests.get(url)
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    return resp

@app.route('/getList', methods=['GET'])
def getList():
    # url = 'http://{0}/records/instance/{1}'.format(auth_get('getUserInfo'),'admin')
    params = dict(request.args)
    idcid = params['idcid'][0]
    logger.debug(idcid)
    url = '{0}/{1}/{2}'.format(auth_get('getList'),'admin',idcid)
    params = {
        'excludes': 'deleted'
    }
    r = requests.get(url, params=params)
    resp = make_response(r.content)
    resp.headers['Content-Type']='text/json'
    return resp


@app.route('/getImage/<string:clu_id>', methods=['GET'])
def getImage(clu_id):
    # url = 'http://{0}/records/images/{1}'.format(auth_get('getUserInfo'),clu_id)

    # url = auth_get('getImage')
    # data = {"cluster_id": clu_id}
    # r = requests.get(url,data)


    url = '{0}/{1}'.format(auth_get('getImage'),clu_id)
    r = requests.get(url)
    #resp = r.json().pop('message')
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    return resp


@app.route('/getIdcReg/<string:reg>')
def getIdcRegFunc(reg):
    #url = 'http://{0}/records/idcs/{1}'.format(auth_get('getUserInfo'),reg)
    #url = 'http://{0}/records/idcs/{1}'.format(auth_get('getUserInfo'),reg)
    url = '{0}/{1}'.format(auth_get('getIdcs'),reg)
    print(url)
    r = requests.get(url)
    resp = r.json()
    print(resp)

    resp = make_response(r.content)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/getIdcClur/<int:clu>')
def getIdcClur(clu):
    # url = 'http://{0}/records/clusters/{1}'.format(auth_get('getUserInfo'), clu)
    url = '{0}/{1}'.format(auth_get('getIdcClur'), clu)
    r = requests.get(url)
    resp = r.json()
    print(resp)

    resp = make_response(r.content)
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/getKeyList',methods=['GET'])
def getKeyList():
    # /keypairs/list?cluster_id={cluster_id}
    params = dict(request.args)

    cluster_id = params['cluster_id'][0]
    url = auth_get('getKeyList')
    values = {
        'cluster_id': cluster_id
    }
    r = requests.get(url, params=values)
    resp = make_response(r.content)
    resp.headers['Content-Type']='application/json'
    return resp

@app.route('/addKey',methods=['POST'])
def addKey():
    url = auth_get('addKey')
    cluster_id = request.form.get('cluster_id')
    key_name = request.form.get('key_name')
    key_content = request.form.get('key_content')

    values = {
        'cluster_id': cluster_id,
        'key_name': key_name,
        'key_content': key_content
    }

    r = requests.post(url,data=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('failed!')
    return resp


@app.route('/set_instance_status', methods=['POST'])
def set_instance_status():
    rds = redis.StrictRedis(host='localhost', port=6381, db=0)
    # DEFAULT_TIMEOUT = 90

    value = request.stream.read()
    print value

    key = json.loads(value).get('instance_id', None)
    if key:
        rds.rpush(key, value)
        # rds.expire(key, DEFAULT_TIMEOUT)

    return 'set key "%s" to value "%s" successfully.' % (key, value)


@app.route('/get_instance_status/<instance_id>', methods=['GET'])
def get_instance_status(instance_id):
    rds = redis.StrictRedis(host='localhost', port=6381, db=0)

    data = rds.blpop(instance_id, 10)
    if data:
        resp = make_response(data[1])
        resp.headers['Content-Type'] = 'application/json'
        return resp
    else:
        return make_response('timeout')
