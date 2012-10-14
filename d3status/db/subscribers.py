# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

from d3status.db import Model
from d3status import consts


class SubscribersModel(Model):
    def subscribe(self, token, categorys, locale="en"):
        row = self.db.get("select * from subscribers where token=%s", token)
        if not row:
            sql = "insert into subscribers (token, categorys, status, locale) " \
            "values (%s, %s, %s, %s)"
            self.db.execute(sql, token, categorys, consts.SUBSCRIBE_STATUS_ON,
                            locale)
        else:
            sql = "update subscribers set categorys=%s, locale=%s where token=%s"
            self.db.execute(sql, categorys, locale, token)

    def unsubscribe(self, token):
        sql = "update subscribers set status=%s where token=%s"
        self.db.execute(sql, consts.SUBSCRIBE_STATUS_OFF, token)

    def get_subscribers(self, limit=200, offset=0):
        return self.db.query("select * from subscribers where status='on' "
                             "limit %s offset %s",
                             limit, offset)
