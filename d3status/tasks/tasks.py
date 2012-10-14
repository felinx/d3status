# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

"""Celery tasks center

Setup env for celery tasks and import them.
"""

import os
import platform
import sys

_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.join(_dir, "..")

try:
    # tornado process
    import d3status
except ImportError:
    # celeryd process runtime env
    if platform.system() == "Linux":
        os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"
    sys.path.append(os.path.join(_root, ".."))
    # append current directory for celeryconfig.py
    sys.path.append(_dir)

    from tornado.options import options
    from tornado.database import Connection

    from d3status.libs.options import parse_options
    parse_options()

    from d3status.db import Model

    # db connection
    db = Connection(host=options.mysql["host"] + ":" +
                            options.mysql["port"],
                         database=options.mysql["database"],
                         user=options.mysql["user"],
                         password=options.mysql["password"],
                         )

    Model.setup_dbs({"db": db})


from d3status.libs.importlib import import_module
from d3status.libs.utils import find_modules


def _load_tasks():
    _current_module = sys.modules[__name__]
    for m in find_modules(os.path.dirname(__file__)):
        if m.endswith("_tasks"):  # xxx_tasks.py
            try:
                mod = import_module("." + m, package="d3status.tasks")
                for func in dir(mod):
                    if func.endswith("_task"):
                        setattr(_current_module, func, getattr(mod, func))
            except ImportError:
                pass

_load_tasks()

