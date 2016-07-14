#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Date : 24/5/16 PM1:02
# Copyright: TradeShift.com
__author__ = 'liming'

import MySQLdb, logging

from app.auth import get as auth_get

logger = logging.getLogger(__name__)

class Db_access(object):

        def __init__(self):
            self._conn, self.cursor = None, None
            self._connect()

        def _connect(self):
            try:
                self._conn = MySQLdb.connect(host=auth_get('mysql_host'), db=auth_get('mysql_db'), user=auth_get('mysql_user'),
                                             passwd=auth_get('mysql_pass'), port=auth_get('mysql_port'), charset='utf8')

                self.cursor = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

            except Exception, e:
                self.msg = 'Error when connect mysql: %s' % e.args
                logger.error(self.msg)

        def connect(self):
            try:
                if not self._conn.ping():
                    logger.debug('Reconnect mysql...')
                    self._connect()
            except Exception:
                logger.debug('Reconnect mysql...')
                self._connect()

        def get(self, sql):
            self.connect()
            print sql
            try:
                self.cursor.execute(sql)

                raw_records = self.cursor.fetchall()

                return 0, list(raw_records)
            except Exception, e:
                logger.error(e.args)
                return 1, []
            finally:
                self.cursor.close()

        def mod(self, sql):
            self.connect()
            try:
                self.cursor.execute(sql)
                c = self._conn.commit()
                return 0, c
            except Exception, e:
                logger.error(e.args)
                return 2, 'sql error'
            finally:
                self.cursor.close()