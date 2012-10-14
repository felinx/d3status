# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012


CELERY_IMPORTS = ("tasks", )

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

BROKER_URL = "redis://%s:%s/%s" % (CELERY_REDIS_HOST, CELERY_REDIS_PORT,
                                   CELERY_REDIS_DB)
