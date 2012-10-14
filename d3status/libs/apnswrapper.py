# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

import time
import traceback
import logging
from apns import APNs, Payload

_ignored_content_keys = ("message",)  # maybe more keys later


class APNsWrapper(APNs):
    def __init__(self, use_sandbox=False, cert_file=None, key_file=None):
        super(APNsWrapper, self).__init__(use_sandbox, cert_file, key_file)
        self._payloads = []

    def append(self, token, notification, alert=None, badge=None, sound=None):
        if not alert:
            alert = notification.get("message", None)

        if alert and isinstance(alert, dict):
            alert = alert.get("message", None)

        for key in _ignored_content_keys:
            try:
                del notification[key]
            except KeyError:
                pass

        payload = Payload(alert, badge, sound, custom=notification)
        self._payloads.append((token, payload))

    def flush(self):
        if self._payloads:
            for token, payload in self._payloads:
                try:
                    self.gateway_server.write(self.gateway_server._get_notification(token, payload))
                except:
                    logging.error(traceback.format_exc())
                    # trigger reconnect
                    self._gateway_connection = None

            self._payloads = []
