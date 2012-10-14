# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

import importlib

_module_instances = {}


def load(root_module, suffix):
    def load_(name):
        name = name.lower()
        key = "%s.%s" % (root_module, name)
        if key not in _module_instances:
            try:
                module = importlib.import_module(".%s" % name, root_module)
            except ImportError:
                module = importlib.import_module(".%s" % name[:-1], root_module)

            # load("breeze.db", "users", "Model") will return UsersModel class obj
            cls = getattr(module,
                          "%s%s%s%s" % (name[0].upper(), name[1:],
                                        suffix[0].upper(), suffix[1:]))
            _module_instances[key] = cls()

        return _module_instances[key]

    return load_
