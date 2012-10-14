# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  May 30, 2012
#

import os

from celery.task import task
from tornado.options import options

from d3status.libs.apnswrapper import APNsWrapper

_root = os.path.join(os.path.dirname(__file__), "..")
_apns = None


@task
def apns_push_task(tokens, notification, alert=None, badge=None, sound=None):
    apns_push(tokens, notification, alert, badge, sound)


def apns_push(tokens, notification, alert=None, badge=None, sound=None):
    _setup_apns()
    if isinstance(tokens, basestring):
        tokens = [tokens, ]

    for token in tokens:
        _apns.append(token, notification, alert, badge, sound)

    _apns.flush()


def _setup_apns():
    global _apns

    if not _apns:
        cert_file = os.path.join(_root, options.apns_certificate)
        if not options.apns_certificate_key:
            key_file = None
        else:
            key_file = os.path.join(_root, options.apns_certificate_key)

        _apns = APNsWrapper(use_sandbox=options.apns_sandbox,
                            cert_file=cert_file,
                            key_file=key_file)
