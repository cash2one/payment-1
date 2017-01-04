#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, requests, json
from hashlib import sha1
from wx_token import wx_shedule
from wechat_settings import WX_PUBLIC, WX_BASE_URL

__author__ = 'raymondlei'

'''
 将token、timestamp、nonce三个参数进行字典序排序
'''

class WXMenu:

    def __init__(self):
        self.__APPID = WX_PUBLIC['APP_ID']
        self.__APPSECRET = WX_PUBLIC['APP_SECRET']
        self.BASE_URL = WX_BASE_URL
        self.__TOKEN = WX_PUBLIC['TOKEN']


    def check_signature(self, signature, timestamp, nonce):

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
        return True if tmp_str != None and tmp_str == signature else False

    def wechat_sha1(self, list_str):

        """
        SHA1加密
        :param list_str:
        :return:
        """

        sha1_str = list_str[0] + list_str[1] + list_str[2]
        return sha1(sha1_str.encode('utf-8')).hexdigest()

    def get_access_tokenurl(self):

        """
        获取access_token链接
        :return:
        """

        return self.BASE_URL+'token?grant_type=client_credential&appid=%s&secret=%s' % (self.__APPID, self.__APPSECRET)

    def get_js_sdk_url(self, access_token):
        return self.BASE_URL+'/ticket/getticket?access_token=%s&type=jsapi' % (access_token,)


    def get_cre_menu_url(self, access_token):

        """
        获取之定义创建菜单链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/create?access_token=%s' % (access_token,)

    def get_menu_url(self, access_token):

        """
        获取自定义菜单查询链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/get?access_token=%s' % (access_token,)

    def remove_menu_url(self, access_token):

        """
        获取自定义菜单删除链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'menu/delete?access_token=%s' % (access_token,)

    def get_current_self_menu_info(self, access_token):

        """
        获取自定义菜单配置链接
        :param access_token:
        :return:
        """

        return self.BASE_URL+'get_current_selfmenu_info?access_token=%s' % (access_token,)

# *******************************************菜单实现***************************************************

    def create_menu(self, body_json):
        """
        创建自定义微信菜单
        :param body: dict
        :return:
        """

        access_token = wx_shedule.get_access_token()
        if access_token:

            url = self.get_cre_menu_url(access_token)
            data = self.create_menu_data(body_json)

            r = requests.post(url, data.encode('utf-8'))

            if r.status_code == 200:
                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单创建接口' + res)
                json_res = json.loads(res)
                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.error('【微信自定义菜单】自定义菜单创建接口获取不到access_token')

    def create_menu_data(self, body_dict):

        """
        微信自定义菜单数据
        :param body_dict 一个菜单字典
        :return:
        """

        menu_dict = {}

        for but, list_but in body_dict.items():

            # 二级菜单
            if isinstance(list_but, list):

                arr = []

                for i in list_but:

                    if i in 'name' or i in 'sub_button':
                        arr.append(i)

                menu_dict[but] = arr

        return json.dumps(menu_dict, ensure_ascii=False)

    def get_menu(self):

        """
        自定义菜单查询接口
        :return:
        """

        access_token = wx_shedule.get_access_token()

        if access_token:

            url = self.get_menu_url(access_token)
            r = requests.get(url)
            logging.debug('【微信自定义菜单】自定义菜单查询接口Response[' + str(r.status_code) + ']')

            if r.status_code == 200:

                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单查询接口' + res)
                json_res = json.loads(res)

                if 'errcode' in json_res.keys():
                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.error('【微信自定义菜单】自定义菜单查询接口获取不到access_token')

    def delete_menu(self):

        """
        自定义菜单删除接口
        :return:
        """

        access_token = wx_shedule.get_access_token()

        if access_token:

            url = self.remove_menu_url(access_token)
            r = requests.get(url)
            logging.debug('【微信自定义菜单】自定义菜单删除接口Response[' + str(r.status_code) + ']')

            if r.status_code == 200:

                res = r.text
                logging.debug('【微信自定义菜单】自定义菜单删除接口' + res)
                json_res = json.loads(res)

                if 'errcode' in json_res.keys():

                    errcode = json_res['errcode']
                    return errcode
        else:
            logging.error('【微信自定义菜单】自定义菜单删除接口获取不到access_token')


wxmenu = WXMenu()

class WXUtil:

    def __init__(self):
        pass

    def get_server_ip_url(self, access_token):

        return WX_BASE_URL+'getcallbackip?access_token=%s' % (access_token,)

    def get_server_ip(self):
        access_token = wx_shedule.get_access_token()
        url = self.get_server_ip(access_token)
        requests.get(url)



wx_util = WXUtil()

if __name__=='__main__':
    wechat = WXMenu()
    print wechat.wechat_sha1('123','aaa', '222')




