#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import requests
import json
import logging

from common.db.redis_db import redis_db
import wx_menu

__author__ = 'raymondlei'

class WXTokenCache:

    """
    微信TOKEN缓存

    """

    _expire_access_token = 7200             # 微信access_token过期时间, 2小时
    _expire_js_token = 30 * 24 * 3600       # 微信js网页授权过期时间, 30天
    KEY_ACCESS_TOKEN = 'access_token'       # 微信全局唯一票据access_token
    KEY_JSAPI_TICKET = 'jsapi_ticket'       # JS_SDK权限签名的jsapi_ticket


    def set_access_cache(self, key, value):

        """
        添加微信access_token验证相关redis
        :param key:
        :param value:
        :return:
        """
        res = redis_db.wx_token.set(key, value)
        redis_db.wx_token.expire(key, self._expire_access_token)

        logging.debug('【微信token缓存】setCache>>>key[' + key + '],value[' + value + ']')

        return res

    def set_js_cache(self, key, value):

        """
        添加网页授权相关redis
        :param key:
        :param value:
        :return:
        """

        res = redis_db.wx_token.set(key, value)
        redis_db.wx_token.expire(key, self._expire_js_token)

        logging.debug('【微信token缓存】setCache>>>key[' + key + '],value[' + value + ']')

        return res

    def get_cache(self, key):

        """
        获取redis
        :param key:
        :return:
        """

        try:

            v = (redis_db.wx_token.get(key)).decode('utf-8')
            logging.debug(v)
            logging.debug('【微信token缓存】getCache>>>key[' + key + '],value[' + v + ']')

            return v

        except Exception as e:

            return e

token_cache = WXTokenCache()   # 微信token缓存实例


class WxShedule(object):

    """
    定时任务调度器

    excute_task                      执行定时器任务
    get_access_token            获取微信全局唯一票据access_token
    get_jsapi_ticket            获取JS_SDK权限签名的jsapi_ticket
    """
    _expire_time_access_token = 7000 * 1000  # token过期时间

    def excute_task(self):

        """
        执行定时器任务
        :return:
        """
        logging.info('【获取微信全局唯一票据access_token】>>>执行定时器任务')
        tornado.ioloop.IOLoop.instance().call_later(0, self.get_access_token)
        tornado.ioloop.PeriodicCallback(self.get_access_token, self._expire_time_access_token).start()
        # tornado.ioloop.IOLoop.current().start()

    def get_access_token(self):

        """
        获取微信全局唯一票据access_token
        :return:
        """

        url = wx_menu.wxmenu.get_access_tokenurl()
        r = requests.get(url)

        logging.info('【获取微信全局唯一票据access_token】Response[' + str(r.status_code) + ']')

        if r.status_code == 200:

            res = r.text
            logging.info('【获取微信全局唯一票据access_token】>>>' + res)
            d = json.loads(res)

            if 'access_token' in d.keys():

                access_token = d['access_token']

                # 添加至redis中
                token_cache.set_access_cache(token_cache.KEY_ACCESS_TOKEN, access_token)
                # 获取JS_SDK权限签名的jsapi_ticket
                self.get_jsapi_ticket()

                return access_token

            elif 'errcode' in d.keys():

                errcode = d['errcode']
                logging.info(
                    '【获取微信全局唯一票据access_token-SDK】errcode[' + errcode + '] , will retry get_access_token() method after 10s')
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)
        else:

            logging.error('【获取微信全局唯一票据access_token】request access_token error, will retry get_access_token() method after 10s')
            tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)

    def get_jsapi_ticket(self):

        """
        获取JS_SDK权限签名的jsapi_ticket
        :return:
        """


        access_token = token_cache.get_cache(token_cache.KEY_ACCESS_TOKEN)

        if access_token:

            url = wx_menu.wxmenu.get_js_sdk_url(access_token)

            r = requests.get(url)

            logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket的Response[' + str(r.status_code) + ']')

            if r.status_code == 200:

                res = r.text
                logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>' + res)
                d = json.loads(res)
                errcode = d['errcode']

                if errcode == 0:

                    jsapi_ticket = d['ticket']
                    # 添加至redis中
                    token_cache.set_access_cache(token_cache.KEY_JSAPI_TICKET, jsapi_ticket)

                else:

                    logging.info('【微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket>>>>errcode[' + errcode + ']')
                    logging.info('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                    tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)

            else:

                logging.info('【微信JS-SDK】request jsapi_ticket error, will retry get_jsapi_ticket() method after 10s')
                tornado.ioloop.IOLoop.instance().call_later(10, self.get_jsapi_ticket)
        else:

            logging.error('''
            微信JS-SDK】获取JS_SDK权限签名的jsapi_ticket时,access_token获取失败, will retry get_access_token() method after 10s
            ''')
            tornado.ioloop.IOLoop.instance().call_later(10, self.get_access_token)

wx_shedule = WxShedule()

if __name__ == '__main__':


    """
    执行定时器
    """
    wx_shedule.excute_task()