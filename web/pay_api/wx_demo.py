#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.route import route
from web.base import BaseRequestHandler
from common.wechat import wx_menu, wx_msg

__author__ = 'raymondlei'


# @route('/wxsignature')
class WXCheckSignatureHandler(BaseRequestHandler):
    """
    微信签名
    """

    def do_get(self):

        """
        微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数
        :return:
        """

        try:

            # 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
            signature = self.get_argument('signature', None)

            # 时间戳
            timestamp = self.get_argument('timestamp', None)

            # 随机数
            nonce = self.get_argument('nonce', None)

            # 随机字符串
            echostr = self.get_argument('echostr', None)

            result = wx_menu.wxmenu.check_signature(signature, timestamp, nonce)

            if result:

                self.write(echostr)

            else:

                self.write_warning('微信sign校验,---校验失败')

        except Exception as e:

            self.write_warning('微信sign校验,---Exception' + str(e))

@route('/wxauthorize')
class WXAuthorizeHandler(BaseRequestHandler):

    """
        接收关注/取关事件推送
    """

    def do_post(self):

        try:

            body = self.request.body
            wx_msg.wx_msg.author(body)

        except Exception as e:

            self.write_warning('微信取关事件推送，---推送失败' + str(e))


@route('/index')
class WXIndexHandler(BaseRequestHandler):
    """
    测试
    """

    def do_get(self):
        self.write('hello world!')

@route('/demo')
class WXDemoHandler(BaseRequestHandler):
    """
    测试
    """

    def get(self):
        self.write('hello kitty!')
