role_action
=====
```
method: post
uri: /tsRole/<string:ts_resourceId>/<string:action>
json return:
{'status': 0, 'message': ${new status}}
example:
curl -X POST 'http://127.0.0.1:9999/tsRole/192.168.100.2[TSCloud]upload01.local/start'
{"status": 0, "message": "stopped"}
```

collect info
====
```
method: post
uri: /tsRole/collect
json return:
{'status': 0, 'message': 
[
{${role 1 all info}},
{${role 2 all info}}
]
}

example:
curl -X POST 'http://127.0.0.1:9999/tsRole/collect'
{
    "status": 0,
    "message": [
        {
            "status": "running",
            "cpu_idle": 99.98,
            "mem": 536870912,
            "stderr_logfile": "",
            "priv_out": null,
            "tag": "testweb:new",
            "owner": "192.168.100.12",
            "logfile": "",
            "mem_idle": 78.99,
            "port": {
                "80/tcp": [
                    {
                        "HostPort": "",
                        "HostIp": "192.168.100.12"
                    }
                ]
            },
            "priv_in": null,
            "uptime": "2016-06-29T04:47:41.554519549Z",
            "disk": null,
            "name": "web2.bwts.com.ct1",
            "disk_idle": 100,
            "pub_in": null,
            "pub_out": null,
            "stdout_logfile": "",
            "error": "",
            "cpu": 3,
            "priv_ip": "192.168.100.12",
            "pub_ip": null
        },
        {
            "status": "running",
            "cpu_idle": 99.98,
            "mem": 536870912,
            "stderr_logfile": "",
            "priv_out": null,
            "tag": "testweb:new",
            "owner": "192.168.100.12",
            "logfile": "",
            "mem_idle": 79.03,
            "port": {
                "80/tcp": [
                    {
                        "HostPort": "",
                        "HostIp": "192.168.100.12"
                    }
                ]
            },
            "priv_in": null,
            "uptime": "2016-06-29T03:19:07.765233392Z",
            "disk": null,
            "name": "web1.bwts.com.ct1",
            "disk_idle": 100,
            "pub_in": null,
            "pub_out": null,
            "stdout_logfile": "",
            "error": "",
            "cpu": 1,
            "priv_ip": "192.168.100.12",
            "pub_ip": null
        }
    ]
}
```

role_upgrade
======
```
method: post
uri: /tsRole/<string:ts_resourceId>/upgrade
para: tag (string)
	  need_restart (int)

json return:
{'status': 0, 'message': ''}
example:
```

role_create
======
```
method: post
uri: /tsRole/create
para: image (string)
      cpu
      mem

json return:
{'status': 0, 'message': ''}
example:
```

role_delete
======
```
method: post
uri: /tsRole/delete
para: tsResourceId

json return:
{'status': 0, 'message': 'Done'}
{'status': 9, 'message': 'error ext'}
example:
```

role_create
======
call
-----
```
example:
        seq = 9
        d = {
        'seq' : seq,
        'tsRoleName' : 'web%s.bwts.ct.com' % seq,
        'roleName' : 'lmapp',
        'cpu' : 1,
        'mem' : int(0.5 * 1024 * 1024 * 1024),
        'image' : '192.168.100.2:5000/testweb:new',
        'port' : [80],
        'env' : {
        'name': 'liming',
        'age': 30,
        },
        }
        r = requests.post(url + uri, {'create_value': json.dumps(d)})
```

return
-----
```
u'status': 0, u'message': u'436885881edc547cd1170d1cba680d1ca8b802ae8bdb9d50bd70b643369c8979'}
or
{'status': 999, 'message': 'error txt'}
```


role_status
===========
call
------
method: GET

```
curl http://127.0.0.1:9999/tsRole/status/bdc693ee3160
```

return
------
```
{
    "status": 0,
    "message": {
        "status": "running",
        "cpu_idle": 99.72,
        "mem": 536870912,
        "stderr_logfile": "",
        "priv_out": null,
        "tag": "testweb:new",
        "owner": "192.168.100.12",
        "logfile": "",
        "mem_idle": 78.63,
        "port": {
            "80/tcp": [
                {
                    "HostPort": "",
                    "HostIp": "192.168.100.12"
                }
            ]
        },
        "priv_in": null,
        "uptime": "2016-06-29 22:11:32",
        "disk": null,
        "name": "web1.bwts.ct.com",
        "disk_idle": 100,
        "pub_in": null,
        "pub_out": null,
        "stdout_logfile": "",
        "error": "",
        "cpu": 1,
        "priv_ip": "192.168.100.12",
        "pub_ip": null
    }
}
```
