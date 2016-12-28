#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

from web.route import route
from web import views_v1
from setting import SERVER_PORT, SERVER_ROOT, BASE_HOST, IS_DEBUG, IS_ZIP, IS_COOKIE_XSRF, COOKIE_SECRET
from common.tools.data import init_log

__author__ = 'swzs'

settings = {
    'static_path': os.path.join(SERVER_ROOT, 'static'),
    'template_path': os.path.join(SERVER_ROOT, 'templates'),
    'gzip': IS_ZIP,
    'debug': IS_DEBUG,
    'cookie_secret': COOKIE_SECRET,
    'xsrf_cookie': IS_COOKIE_XSRF,
}

if __name__ == "__main__":

    init_log()
    application = tornado.web.Application(route.handlers, **settings)
    application.listen(SERVER_PORT, address=BASE_HOST, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()
