# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#

try:
    import importlib
except:
    from d3status.libs import importlib

from tornado.options import options
from tornado.web import url
from d3status.handler import APIErrorHandler

handlers = []
ui_modules = {}

# the module names in handlers folder
handler_names = ["status", ]


def _generate_handler_patterns(root_module, handler_names, prefix=options.app_url_prefix):
    for name in handler_names:
        module = importlib.import_module(".%s" % name, root_module)
        module_hanlders = getattr(module, "handlers", None)
        if module_hanlders:
            _handlers = []
            for handler in module_hanlders:
                try:
                    patten = r"%s%s" % (prefix, handler[0])
                    if len(handler) == 2:
                        _handlers.append((patten,
                                          handler[1]))
                    elif len(handler) == 3:
                        _handlers.append(url(patten,
                                             handler[1],
                                             name=handler[2])
                                         )
                    else:
                        pass
                except IndexError:
                    pass

            handlers.extend(_handlers)

_generate_handler_patterns("d3status.handlers", handler_names)

# Override Tornado default ErrorHandler
handlers.append((r".*", APIErrorHandler))
