#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from hashlib import sha1, md5

# import wechatpy
# from wechatpy.utils import check_signature
# from wechatpy.exceptions import InvalidSignatureException

from wechat_settings import APP_ID, APP_SECRET, BASE_URL, WECHAT_TOKEN

__author__ = 'raymondlei'

'''
 将token、timestamp、nonce三个参数进行字典序排序
'''

class WechatInterface:

    def __init__(self):
        self.__APPID = APP_ID
        self.__APPSECRET = APP_SECRET
        self.BASE_URL = BASE_URL
        self.__TOKEN = WECHAT_TOKEN


    def checkSignature(self, signature, timestamp, nonce):

        """
        验证签名的有效性
        :param token:
        :param timestamp:
        :param nonce:
        :return:
        """
        list_str = [self.__TOKEN, timestamp, nonce]

        #1.将token、timestamp、nonce三个参数进行字典序排序
        list_str.sort()

        #2. 将三个参数字符串拼接成一个字符串进行sha1加密
        tmp_str = self.wechat_sha1(list_str)
        logging.debug('sha1=' + tmp_str + '&signatureure=' + signature)

        # 3. 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
        result = True if tmp_str != None and tmp_str == signature else False
        return result

    def wechat_sha1(self, list_str):
        sha1_str = list_str[0] + list_str[1] + list_str[2]
        return sha1(sha1_str.encode('utf-8')).hexdigest()

    def get_access_tokenurl(self):

        """
        获取access_token链接
        :return:
        """

        return self.BASE_URL+'token?grant_type=client_credential&appid=%s&secret=%s' % (self.__APPID, self.__APPSECRET)

    def get_menu_url(self, access_token):

        """
        获取之定义创建菜单链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/create?access_token=%s' % (access_token,)

    def getMenuURL(self, access_token):

        """
        获取自定义菜单查询链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/get?access_token=%s' % (access_token,)

    def removeMenuURL(self, access_token):

        """
        获取自定义菜单删除链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/delete?access_token=%s' % (access_token,)

    def getCurrentSelfmenuInfo(self, access_token):

        """
        获取自定义菜单配置链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'get_current_selfmenu_info?access_token=%s' % (access_token,)




wechat_func = WechatInterface()


if __name__=='__main__':
    wechat = WechatInterface()
    print wechat.wechat_sha1('123','aaa', '222')




