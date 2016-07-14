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

from . import app


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
    idcs = getIdcs()

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
    return render_template('indexPage.html')


@app.route('/logout')
def logout():
    # redirect_to = urllib.quote(auth_get('local'), '')
    redirect_to = auth_get('local')
    return redirect('%s?service=%s' % (auth_get('logout_url'), redirect_to))



@app.route('/login/<string:route>')
def login(route):
    redirect_to = urllib.quote('{0}/{1}'.format(auth_get('local'), route), '')
    return redirect('%s?service=%s' % (auth_get('auth_url'), redirect_to))


@app.route('/tasklogdetail')
def tasklogdetail():
    pageFlag = 'tasklogdetail'
    logger.debug("tasklogdetail PageFlag="+pageFlag+",username="+profilename)

    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/tasklogdetail'.format(auth_get("local"))),
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
            
            resp = redirect('/tasklogdetail')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('ts_service.html', flag=pageFlag, username=profilename)


@app.route('/detailsearch')
def detailsearch():
    pageFlag = 'detailsearch'

    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/detailsearch'.format(auth_get("local"))),
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
            
            resp = redirect('/detailsearch')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('ts_service.html', flag=pageFlag, username=profilename)

@app.route('/qcloud')
def qcloud():
    pageFlag = 'qcloud'

    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/qcloud'.format(auth_get("local"))),
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
            
            resp = redirect('/qcloud')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('ts_service.html', flag=pageFlag, username=profilename)


@app.route('/list',methods=['POST'])
def showList():
    query_start_time = request.form['query_start_time']
    query_end_time = request.form['query_end_time']
    limit_start = request.form['limit_start']
    limit_end = request.form['limit_end']

    values={'query_start_time': query_start_time,
            'query_end_time': query_end_time,
            'limit_start': limit_start,
            'limit_end': limit_end}
    headers = {
        'content-type': 'application/json',
        "Accept": "application/json",
    }

    url = 'http://{0}/cdn/tasklog/search'.format(auth_get('task_log_search'))
    logger.debug("url============="+url)

    r = requests.post(url, json=values, headers=headers)
    resp = make_response(r.content)
    resp.headers['Content-Type'] = 'text/json'
    return resp


@app.route('/searchdetaillist', methods=['POST'])
def detailSearchList():
    project_name = None if request.form.get('programName') is '' else request.form.get('programName')
    file_name = None if request.form.get('fileName') is '' else request.form.get('fileName')
    status = None if request.form.get('fileStatus') is '' else request.form.get('fileStatus')
    download_url = None if request.form.get('fileLink') is '' else request.form.get('fileLink')
    start_time = None if request.form.get('start_time') is '' else request.form.get('start_time')
    fromIndex = None if request.form.get('from') is '' else request.form.get('from')
    size = 10 if request.form.get('size') is '' else request.form.get('size')

    values={'project_name': project_name,
            'file_name': file_name,
            'status': status,
            'download_url': download_url,
            'start_time': start_time,
            'size': size,
            'from': fromIndex}

    logger.debug(values)

    url = auth_get('detailSearch')

    r = requests.post(url, data=values)
    resp = make_response(r.content)
    resp.headers['Content-Type'] = 'text/json'
    return resp


@app.route('/detail/<string:task_id>/<int:task_status>')
def showDetail(task_id, task_status):
    url = 'http://{0}/admin/cdn/tasks/{1}/{2}'.format(auth_get('task_log_detail'), task_id, task_status)
    logger.debug('url: %s', url)
    try:
        r = requests.get(url)

        if r.ok:
            resp = make_response(r.content)
            resp.headers['Content-Type'] = 'text/json'
        else:
            data = json.dumps({'status': 1, 'content': '%s => %s' % (url, r.reason) }, ensure_ascii=False)
            resp = make_response(data)
            resp.headers['Content-Type'] = 'text/json'
    except Exception, e:
        data = json.dumps({'status': 1, 'content': 'get %s:' % url + str(e)}, ensure_ascii=False)
        resp = make_response(data)
        resp.headers['Content-Type'] = 'text/json'

    return resp

@app.route('/detail/<string:task_id>')
def showDetail1(task_id):
    url = 'http://{0}/admin/cdn/tasks/{1}'.format(auth_get('task_log_detail'), task_id)
    logger.debug('url: %s', url)
    try:
        r = requests.get(url)

        if r.ok:
            resp = make_response(r.content)
            resp.headers['Content-Type'] = 'text/json'
        else:
            data = json.dumps({'status': 1, 'content': '%s => %s' % (url, r.reason) }, ensure_ascii=False)
            resp = make_response(data)
            resp.headers['Content-Type'] = 'text/json'
    except Exception, e:
        data = json.dumps({'status': 1, 'content': 'get %s:' % url + str(e)}, ensure_ascii=False)
        resp = make_response(data)
        resp.headers['Content-Type'] = 'text/json'

    return resp


@app.route('/searchdetail/<string:task_id>')
def showSearchDetail(task_id):
    url = '{0}/{1}'.format(auth_get('detailSearch'), task_id)

    try:
        r = requests.get(url)

        if r.ok:
            resp = make_response(r.content)
            resp.headers['Content-Type'] = 'text/json'
        else:
            data = json.dumps({'status': 1, 'content': '%s => %s' % (url, r.reason) }, ensure_ascii=False)
            resp = make_response(data)
            resp.headers['Content-Type'] = 'text/json'
    except Exception, e:
        data = json.dumps({'status': 1, 'content': 'get %s:' % url + str(e)}, ensure_ascii=False)
        resp = make_response(data)
        resp.headers['Content-Type'] = 'text/json'

    return resp


@app.route('/vm_create')
def show_vm_create():
    idcs = getIdcs()
    pageFlag = 'vm_create'
    profilename = 'admin'
    logger.debug("create PageFlag="+pageFlag)

    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/vm_create'.format(auth_get("local"))),
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
            
            resp = redirect('/vm_create')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('ts_service.html', flag=pageFlag, idcs=idcs, username=profilename)


def request_new_ip(cluster_id):
    # url = 'http://{0}/ip'.format(auth_get('get_public_ip'))
    url = auth_get('get_public_ip')
    r = requests.get(url, data={'cluster_id': cluster_id})
    print cluster_id
    print r.content
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


@app.route('/getIdcs')
def getIdcs():
    # url = 'http://{0}/records/idcs'.format(auth_get('getUserInfo'))
    url = auth_get('getIdcs')
    r = requests.get(url)
    resp = r.json().pop('message')
    print(resp)
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
