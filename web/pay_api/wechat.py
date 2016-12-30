#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from web.route import route
from web.base import BaseRequestHandler
from common.wechat.WechatInterface import wechat_func
import wechatpy



__author__ = 'raymondlei'


@route('/wxsignature')
class WechatCheckSignatureHandler(BaseRequestHandler):

    def do_get(self):

        """
        微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数
        :return:
        """

        try:

            # 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
            signature = self.get_body_argument('signature', None)

            # 时间戳
            timestamp = self.get_body_argument.get('timestamp', None)

            # 随机数
            nonce = self.get_body_argument.get('nonce', None)

            # 随机字符串
            echostr = self.get_body_argument.get('echostr', None)

            result = wechat_func.checkSignature(signature, timestamp, nonce)

            if result:

                logging.debug('微信sign校验,返回echostr='+echostr)
                self.write(echostr)

            else:

                self.write_warning('微信sign校验,---校验失败')

        except Exception as e:
            self.write_warning('微信sign校验,---Exception' + str(e))


