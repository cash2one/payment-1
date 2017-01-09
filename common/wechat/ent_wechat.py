#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
微信企业号
'''
import logging

from web.route import route
from web.base import BaseRequestHandler

#微信第三方库
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException

from common.wechat.wechat_settings import WX_ENT

__author__ = 'raymondlei'


class EnterpriseSignatureHandler(BaseRequestHandler):
    """
    验证请求有效性
    """
    def do_get(self):

        crypto = WeChatCrypto(WX_ENT['TOKEN'], WX_ENT['ENCODING_AESKEY'], WX_ENT['CORP_ID'])

        try:
            # 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
            signature = self.get_argument('signature', None)

            # 时间戳
            timestamp = self.get_argument('timestamp', None)

            # 随机数
            nonce = self.get_argument('nonce', None)

            # 随机字符串
            echostr = self.get_argument('echostr', None)

            echo_str = crypto.check_signature(
                signature,
                timestamp,
                nonce,
                echostr
            )
            if echo_str:
                self.write(echo_str)
            else:
                logging.debug('微信企业号验证请求有效性失败!')

        except InvalidSignatureException as e:

            raise '微信企业号验证请求有效性异常' +str(e)

