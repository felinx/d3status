# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

from d3status.handler import APIHandler
from d3status.db import load_model
from d3status import consts
from d3status.tasks import status_tasks


class StatusIndexHandler(APIHandler):
    def get(self):
        self.finish(load_model('status').get_status())


class StatusSubscribeHandler(APIHandler):
    def post(self):
        token = self.get_argument("deviceToken", "")
        categorys = self.get_argument("categorys", "").split(",")
        categorys = [c for c in categorys if c in consts.CATEGORYS]
        categorys = ",".join(categorys)
        locale = self.get_argument("locale", "en")
        if locale not in consts.LOCALES:
            locale = "en"

        if token:
            load_model("subscribers").subscribe(token, categorys, locale)


class StatusUnsubscribeHandler(APIHandler):
    def post(self):
        token = self.get_argument("deviceToken", "")
        if token:
            load_model("subscribers").unsubscribe(token)


handlers = [(r"/status", StatusIndexHandler),
            (r"/status/subscribe", StatusSubscribeHandler),
            (r"/status/unsubscribe", StatusUnsubscribeHandler),
            ]
