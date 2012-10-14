# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#
"""Project settings"""

import platform
import os

# can't use __file__ directly here because it's parsed by tornado.options
import d3status
root_dir = os.path.dirname(os.path.abspath(d3status.__file__))

if platform.node() == "FELINX":  # FELINX is the hosting server name.
    debug = False
else:
    debug = True

loglevel = "INFO"  # for celeryd
port = 8888

d3_server_status_url = "http://us.battle.net/d3/en/status"

sitename = "D3 Status"
domain = "api.feilong.me"
home_url = "http://%s/d3" % domain
login_url = "http://%s/login" % home_url
app_url_prefix = "/d3/v1"
email_from = "%s <noreply@%s>" % (sitename, domain)
admins = ("Felinx <felinx.lee@gmail.com>",)
send_error_email = True
cookie_secret = "d1d87395-8272-4749-b2f2-dcabd3903a1c"
xsrf_cookies = False

# Apple push notification settings
apns_sandbox = debug
apns_certificate = "d3status_apns_dev.pem"
apns_certificate_key = None

mysql = {"host": "localhost",
         "port": "3306",
         "database": "d3status",
         "user": "felinx",
         "password": "felinx"
         }

smtp = {"host": "localhost",
        "user": "",
        "password": "",
        "duration": 30,
        "tls": False
        }
