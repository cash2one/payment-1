#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.route import route
from web.base import BaseRequestHandler

__author__ = 'raymondlei'

@route('/index')
class TestUrlHandler(BaseRequestHandler):

    def do_get(self):
        print 'aaaaaaa'
        self.write('1231231231231231231')