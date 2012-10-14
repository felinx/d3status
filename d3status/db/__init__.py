# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

from d3status.libs.loader import load

load_model = load("d3status.db", "Model")


class Model(object):
    _dbs = {}

    @classmethod
    def setup_dbs(cls, dbs):
        cls._dbs = dbs

    @property
    def dbs(self):
        return self.dbs

    # legacy support
    @property
    def db(self):
        return self._dbs.get("db", None)
