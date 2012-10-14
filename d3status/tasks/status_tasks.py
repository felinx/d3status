# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jul 2, 2012
#

import os
import tornado.locale

from celery.task import task
from tornado.options import options
from d3status.db import load_model
from d3status.tasks import apns_tasks


@task
def status_notification_task(changed_status):
    status_notifciation(changed_status)


def status_notifciation(changed_status):
    notifications = {}
    for category, services in changed_status.iteritems():
        for name, st in services.iteritems():
            # just push notification about game server now
            if name == "GameServer":
                notifications[category] = st

    for category, st in notifications.iteritems():
        status = "Available" if st else "Unavailable"

        offset = 0
        limit = 200
        while True:
            subscribers = load_model("subscribers").get_subscribers(limit, offset)
            if not subscribers:
                break

            for subscribe in subscribers:
                if category in subscribe.categorys:
                    alert = _trans_alert("Diablo3 %s server status has changed to %s",
                                         category, status, subscribe.locale)
                    apns_tasks.apns_push_task.delay(subscribe.token, {},
                                                    alert=alert, badge=1,
                                                    sound="default")
            offset += len(subscribers)


def _trans(s, locale):
    locale = tornado.locale.get(locale)
    s = locale.translate(s).strip("\"")

    return s


def _trans_alert(alert, category, status, locale):
    def _(s):
        return _trans(s, locale)

    return _(alert) % (_(category), _(status))


_i18n_dir = os.path.join(os.path.join(os.path.dirname(__file__), ".."), 'i18n')
tornado.locale.load_translations(_i18n_dir)
