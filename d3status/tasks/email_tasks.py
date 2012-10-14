# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

from celery.task import task
from d3status.mail import send_email


@task
def send_email_task(fr, to, subject, body, html=None, attachments=[]):
    send_email(fr, to, subject, body, html, attachments)
