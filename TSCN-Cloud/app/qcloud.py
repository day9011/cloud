from . import app
from app.auth import get as auth_get
import requests
from flask import (request,
                   render_template,
                   make_response)

@app.route('/getQcloudList', methods=['POST'])
def getQcloudList():
    getRegionList()
    url = auth_get('q_vm_list')
    region = request.form.get('region')
    values = {
        'region': region
    }
    r = requests.post(url, json=values)

    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('getQcloudList failed')

    return resp


@app.route('/getRegionList', methods=['POST'])
def getRegionList():
    url = auth_get('q_vm_region')
    r = requests.post(url)

    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('getRegionList failed')

    return resp


@app.route('/getZoneList', methods=['POST'])
def getZoneList():
    url = auth_get('q_vm_zone')
    region = request.form.get('region')
    values = {
        "region": region
    }
    print values
    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('get Zone List failed')

    return resp


@app.route('/getImageList', methods=['POST'])
def getImageList():
    url = auth_get('q_vm_image')
    imageType = request.form.get('imageType')
    values = {
        "imageType": imageType
    }
    print values
    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('get Image List failed')

    return resp


@app.route('/getQKeyList', methods=['POST'])
def getQKeyList():
    url = auth_get('q_vm_key')
    r = requests.post(url)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('get Key List failed')

    return resp


@app.route('/getSecuritygroupList', methods=['POST'])
def getSecuritygroupList():
    url = auth_get('q_vm_securitygroup')
    r = requests.post(url)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('get Securitygroup List failed')

    return resp


@app.route('/qStartVM', methods=['POST'])
def startVM():
    url = auth_get('q_vm_start')
    region = request.form.get('region')
    instanceIds = request.form.get('instanceIds')
    values = {
        'Region': region,
        'instanceIds.1': instanceIds
    }
    print values
    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Start VM failed')

    return resp

@app.route('/qStopVM', methods=['POST'])
def stopVM():
    url = auth_get('q_vm_stop')
    region = request.form.get('region')
    instanceIds = request.form.get('instanceIds')
    values = {
        'Region': region,
        'instanceIds.1': instanceIds
    }
    print values
    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Stop VM failed')

    return resp


@app.route('/qCreateVM', methods=['POST'])
def createVM():
    url = auth_get('q_vm_runinstance')
    imageId = request.form.get('imageId')
    cpu = request.form.get('cpu')
    mem = request.form.get('mem')
    storageSize = request.form.get('storageSize')
    period = request.form.get('period')
    imageType = request.form.get('imageType')
    bandwidth = request.form.get('bandwidth')
    storageType = request.form.get('storageType')
    goodsNum = request.form.get('goodsNum')
    zoneId = request.form.get('zoneId')
    keyId = request.form.get('keyId')
    values = {
        'imageId': imageId,
        'cpu': cpu,
        'mem': mem,
        'storageSize': storageSize,
        'period': period,
        'imageType': imageType,
        'bandwidth': bandwidth,
        'storageType': storageType,
        'goodsNum': goodsNum,
        'zoneId': zoneId,
        'keyId': keyId
    }

    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Create VM failed')

    return resp


@app.route('/countPrice', methods=['POST'])
def countPrice():
    url = auth_get('q_vm_price')
    instanceType = 1
    imageId = request.form.get('imageId')
    cpu = request.form.get('cpu')
    mem = request.form.get('mem')
    storageSize = request.form.get('storageSize')
    period = request.form.get('period')
    imageType = request.form.get('imageType')
    bandwidth = request.form.get('bandwidth')
    storageType = request.form.get('storageType')
    goodsNum = request.form.get('goodsNum')
    values = {
        'instanceType': instanceType,
        'imageId': imageId,
        'cpu': cpu,
        'mem': mem,
        'storageSize': storageSize,
        'period': period,
        'imageType': imageType,
        'bandwidth': bandwidth,
        'storageType': storageType,
        'goodsNum': goodsNum
    }

    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Query price failed')

    return resp

@app.route('/importkeypair', methods=['POST'])
def importkeypair():
    url = auth_get('q_vm_importkeypair')
    keyName = request.form.get('keyName')
    pubKey = request.form.get('pubKey')
    values = {
        'keyName': keyName,
        'pubKey': pubKey
    }

    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Import Key failed')

    return resp


@app.route('/setautorenew', methods=['POST'])
def setautorenew():
    url = auth_get('q_vm_setautorenew')
    instanceType = request.form.get('instanceType')
    instanceIds = request.form.get('instanceIds')
    autoRenew = request.form.get('autoRenew')
    values = {
        'instanceType': instanceType,
        'instanceIds.1': instanceIds,
        'autoRenew': autoRenew
    }

    r = requests.post(url, json=values)
    if r.ok:
        resp = make_response(r.content)
    else:
        resp = make_response('Set auto renew failed')

    return resp


@app.route('/construction')
def construction():
    
    ticket = request.args.get('ticket', None)
    if ticket:
        params = [
            ('service', '{0}/construction'.format(auth_get("local"))),
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
            
            resp = redirect('/construction')
            resp.set_cookie('username', username)
            return resp
        except Exception as e:
            print 'error: ', str(e)

    return render_template('buildingPage.html')