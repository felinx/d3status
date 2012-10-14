# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jul 2, 2012
#

import os
import platform
import sys
import logging
from pyquery import PyQuery as pq
from lxml import etree

from tornado.httpclient import HTTPRequest, HTTPClient
from tornado.options import options

_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_dir, "..")
# append tasks directory for celeryconfig.py
sys.path.append(os.path.join(_root, "tasks"))

try:
    # tornado process
    import d3status
except ImportError:
    # celeryd process runtime env
    if platform.system() == "Linux":
        os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"
    sys.path.append(os.path.join(_root, ".."))

from tornado.options import options
from tornado.database import Connection

from d3status.libs.options import parse_options
parse_options()

from d3status.db import Model
from d3status.db import load_model
from d3status.mail import send_email
from d3status.tasks import status_tasks

# db connection
db = Connection(host=options.mysql["host"] + ":" +
                        options.mysql["port"],
                     database=options.mysql["database"],
                     user=options.mysql["user"],
                     password=options.mysql["password"],
                     )

Model.setup_dbs({"db": db})


def update_server_status():
    url = options.d3_server_status_url
    req = HTTPRequest(url=url)

    client = HTTPClient()
    response = client.fetch(req)
    if response.code == 200:
        status = _parse_server_status(response.body)
        changed_status = load_model("status").update_status(status)
        if changed_status:
            status_tasks.status_notification_task.delay(changed_status)
    else:
        err = "GET_D3_SERVER_STAUTS_ERROR: %s\n%s" (response.code, response)
        logging.error(err)

        # send email
        subject = "[%s]Get D3 server status error" % options.sitename
        body = err
        if options.send_error_email:
            send_email(options.email_from, options.admins, subject, body)


def _parse_server_status(body):
    status = {}

    q = pq(etree.fromstring(body))
    boxes = q(".box")  # category box
    for box in boxes:
        box_q = pq(etree.fromstring(etree.tostring(box)))
        category = box_q(".category")[0].text.strip()
        status[category] = {}
        servers = box_q(".server")
        for server in servers:
            server_q = pq(etree.fromstring(etree.tostring(server)))
            server_name = server_q(".server-name")[0].text.strip().replace(" ", "")
            if server_name:
                status_icon = server_q(".status-icon")[0]
                class_ = status_icon.get("class")
                if class_:
                    st = 0
                    if "up" in class_:
                        st = 1
                    status[category][server_name] = st

    return status


if __name__ == "__main__":
    update_server_status()
