#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 25/5/16 PM11:15
# Copyright: TradeShift.com
__author__ = 'liming'

import logging


class ColorHandler(logging.StreamHandler):
    LEVEL_COLORS = {
        logging.DEBUG: '\033[00;32m',  # GREEN
        logging.INFO: '\033[00;36m',  # CYAN
        # logging.AUDIT: '\033[01;36m',  # BOLD CYAN
        logging.WARN: '\033[01;33m',  # BOLD YELLOW
        logging.ERROR: '\033[00;31m',  # RED
        logging.CRITICAL: '\033[01;31m',  # BOLD RED
        'end': '\x1b[0m',
    }

    def format(self, record):
        record.color = self.LEVEL_COLORS[record.levelno]
        record_str = logging.StreamHandler.format(self, record)
        return record.color + record_str + self.LEVEL_COLORS['end']
