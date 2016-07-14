#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 1/6/16 PM3:40
# Copyright: TradeShift.com
__author__ = 'liming'

import time
from logging import config as logging_config
from app.auth import get as get_auth
from app.auth import init_auth
from app.utils.daemond import be_daemon
from app.utils.parse import get_options

from collector.collector import info_collect



init_auth('conf/config.yml')

# be_daemon()

def config_logging(log_cfg):
    logging_config.fileConfig(log_cfg)

def handler():
    info_collect()


if __name__ == '__main__':
    config_logging('conf/collector_logging.ini')
    parser, opts = get_options()

    if opts.daemon:
        be_daemon()

    while True:
        handler()
        print 'time sleep'
        time.sleep(get_auth('monitor_interval'))

    info_collect()

