#!/usr/bin/env python
# -*- coding: utf-8 -*-

from web.route import route
from web.base import BaseRequestHandler
from common.wechat import wx_menu, wx_token

"""
   微信公众号
"""
__author__ = 'raymondlei'


@route('/demo/wxsignature')
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

            self.write_warning('微信sign校验异常' + str(e))

@route('/wxtoken')
class WXGetAccessTokenHandler(BaseRequestHandler):

    """
    获取全局唯一的ACCESSTOKEN
    """

    def do_get(self):

        try:

            access_token = wx_token.wx_shedule.get_access_token()
            self.write(access_token)

        except Exception as e:
            self.write_warning('微信获取全局唯一ACCESSTOKEN异常'+ str(e))

@route('/wxiplist')
class WXServerIPHandler(BaseRequestHandler):

    """
    获取微信服务器的IP地址
    """

    def do_get(self):

        try:

            res = wx_menu.wx_util.get_server_ip()
            self.write(res)

        except Exception as e:
            self.write_warning('微信获取服务器IP地址异常'+ str(e))

@route('/wxmenu')
class WXMenuHandler(BaseRequestHandler):

    """
    微信公众号自定义菜单
    """

    def do_post(self):

        """
        创建自定义菜单
        :return:
        """

        try:
            body_json = self.get_json_request_body()
            res = wx_menu.wxmenu.create_menu(body_json)
            self.write(res)
        except Exception as e:
            self.write_warning("创建微信自定义菜单异常"+ str(e))



    def do_get(self):

        """
        自定义菜单查询
        :return:
        """

        pass