# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 feilong.me. All rights reserved.
#
# @author: Felinx Lee <felinx.lee@gmail.com>
# Created on  Jun 30, 2012
#


import os
import platform
import sys

if platform.system() == "Linux":
    os.environ["PYTHON_EGG_CACHE"] = "/tmp/egg"
_root = os.path.dirname(os.path.abspath(__file__))
# append tasks directory for celeryconfig.py
sys.path.append(os.path.join(_root, "tasks"))
# chdir to current directory
# workaround for d3status-redis27 server which raise exception(celeryd use os.getcwd())
# when using supervisor to run app.py
os.chdir(_root)

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options
from tornado.database import Connection

try:
    import d3status
except ImportError:
    import sys
    sys.path.append(os.path.join(_root, ".."))

from d3status.libs.options import parse_options


class Application(web.Application):
    def __init__(self):
        from d3status.urls import handlers, ui_modules
        from d3status.db import Model

        settings = dict(debug=options.debug,
                        template_path=os.path.join(os.path.dirname(__file__),
                                                   "templates"),
                        static_path=os.path.join(os.path.dirname(__file__),
                                                 "static"),
                        login_url=options.login_url,
                        xsrf_cookies=options.xsrf_cookies,
                        cookie_secret=options.cookie_secret,
                        ui_modules=ui_modules,
                        #autoescape=None,
                        )

        # d3status db connection
        self.db = Connection(host=options.mysql["host"] + ":" +
                                options.mysql["port"],
                             database=options.mysql["database"],
                             user=options.mysql["user"],
                             password=options.mysql["password"],
                             )

        Model.setup_dbs({"db": self.db})

        super(Application, self).__init__(handlers, **settings)

    def reverse_api(self, request):
        """Returns a URL name for a request"""
        handlers = self._get_host_handlers(request)

        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name

        return None


def main():
    parse_options()

    http_server = HTTPServer(Application(),
                             xheaders=True)
    http_server.bind(int(options.port), "127.0.0.1")  # listen local only
    http_server.start(1)

    IOLoop.instance().start()

if __name__ == '__main__':
    main()
