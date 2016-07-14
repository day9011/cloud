# -*- coding: utf-8 -*-
"""
    core.auth
    ~~~~~~~~~
    Auth info management.
    :copyright: (c) 2015 by Yu Jianjian
    :license: iqiyi.com
"""
import yaml
import copy
__all__ = ['init_auth', 'get', 'gets', 'dump_all', 'auth_clone']
_AUTH_ = None
def init_auth(cfg_path):
    global _AUTH_
    with open(cfg_path) as f:
        cfg = yaml.load(f)
    _AUTH_ = cfg
    return dump_all()
def get(key_name, default=None):
    return _AUTH_.get(key_name, default)
def gets(*keys):
    _auths = []
    for k in keys:
        _auths.append((k, get(k)))
    return dict(_auths)
def dump_all():
    return copy.deepcopy(_AUTH_)
auth_clone = (lambda: copy.deepcopy(_AUTH_))
