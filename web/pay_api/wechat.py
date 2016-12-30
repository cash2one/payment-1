#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.route import route
from web.base import BaseRequestHandler
import wechatpy

__author__ = 'raymondlei'


@route('/signature')
class WechatCheckSignatureHandler(BaseRequestHandler):

    def do_get(self):
        print 'signature'
        self.write('check check signature')