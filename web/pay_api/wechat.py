#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.route import route
from web.base import BaseRequestHandler
import wechatpy

__author__ = 'raymondlei'


@route('/checkSignature')
class WechatCheckSignatureHandler(BaseRequestHandler):

    def do_post(self, *args, **kwargs):
        pass