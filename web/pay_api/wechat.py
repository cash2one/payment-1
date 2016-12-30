#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from web.route import route
from web.base import BaseRequestHandler

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from common.wechat.WechatInterface import wechat_func
from common.wechat.wechat_settings import WECHAT_TOKEN


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

            result = wechat_func.checkSignature(signature, timestamp, nonce)

            if result:

                self.write(echostr)

            else:

                self.write_warning('微信sign校验,---校验失败')

        except Exception as e:
            self.write_warning('微信sign校验,---Exception' + str(e))


@route('/wxsignature')
class WXCheckSignatureHandler(BaseRequestHandler):

    def do_get(self):
        try:
            # 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
            signature = self.get_argument('signature', None)

            # 时间戳
            timestamp = self.get_argument('timestamp', None)

            # 随机数
            nonce = self.get_argument('nonce', None)

            # 随机字符串
            echostr = self.get_argument('echostr', None)

            result = check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
            print type(result), result
            if result:
                self.write(echostr)
            else:
                self.write_warning('微信sign校验,---校验失败')
        except InvalidSignatureException as e:
            self.write_warning('微信sign校验,---Exception' + str(e))