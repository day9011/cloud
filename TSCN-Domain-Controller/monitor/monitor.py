# -*- coding:utf-8 -*-
__author__ = 'liming'

import os
import time

from daemond import be_daemon
from auth import get as get_auth
from auth import init_auth
from utils.parse import get_options

cfg_path = os.path.abspath(os.path.pardir) + '/config.yml'

init_auth(cfg_path)

import status

# be_daemon()

def handler():
    status.main()

def main():
    while True:
        handler()
        time.sleep(get_auth('monitor_interval'))


if __name__ == '__main__':
    parser, opts = get_options()

    if opts.daemon:
        be_daemon()

    main()
