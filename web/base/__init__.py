#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import tornado
from tornado.web import RequestHandler, HTTPError
from biz_exception import BizError
from error_exception import E_FAILED, E_OK, S_ERROR
import setting
import sys

"""
api基类
"""

__author__ = 'swzs'

class BaseRequestHandler(RequestHandler):


    def do_get(self, *args, **kwargs):
        raise HTTPError(405)

    def do_post(self, *args, **kwargs):
        raise HTTPError(405)

    def do_put(self, *args, **kwargs):
        raise HTTPError(405)

    def do_delete(self, *args, **kwargs):
        raise HTTPError(405)

    def get(self, *args, **kwargs):
        try:
            self.do_get(*args, **kwargs)
        except Exception, e:
            self.__handle_exception(e)
        else:
            self.__handle_exception()

    def post(self, *args, **kwargs):
        try:
            self.do_post(*args, **kwargs)
        except Exception, e:
            self.__handle_exception(e)
        else:
            self.__handle_exception()

    def put(self, *args, **kwargs):
        try:
            self.do_put(*args, **kwargs)
        except Exception, e:
            self.__handle_exception(e)
        else:
            self.__handle_exception()

    def delete(self, *args, **kwargs):
        try:
            self.do_delete(*args, **kwargs)
        except Exception, e:
            self.__handle_exception(e)
        else:
            self.__handle_exception()


    # def options(self, *args, **kwargs):
    #     """
    #     @author:Sven
    #     主要是辅助前段浏览器实现跨域访问
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     self.write_success("OK")
    #
    #
    # def head(self, *args, **kwargs):
    #     """
    #     @author : sven
    #     主要是辅助前段浏览器实现跨域访问
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     self.write_success("OK")

    def get_account_id(self):
        """
        取得当前用户的id, 如果用户当前不在线，则返回0
        注意:这里如果是用作单元测试的时候需要给一个默认的ID或者一条完整的数据,
        譬如说: header 里面的 Token,以及需要登录后的完整逻辑
        """
        token = self.request.headers.get("token", "")
        if token == '':
            return 0

        return

    def get_request_since(self):
        """
        针对一些按TimeLine相关的api，需要客户端提供一个since header，表示取 自从since 以后的数据
        """

        return int(self.request.headers.get("since", "0"))

    def get_json_request_body(self):
        """
        如果前端请求body是json格式的数据时处理
        """
        return tornado.escape.json_decode(self.request.body)

    def write_warning(self, message):
        """
        发送警告消息
        :param message:
        :return:

        if setting.IS_DEBUG:
            self.write({"_result": False, "message": message})
        else:
            self.write({"_result": False})
        """
        self.http_mothods_result["success"] = False
        self.http_mothods_result["message"] = message
        self.write(self.http_mothods_result)

        return

    def write_success(self, result="OK"):
        """
        发送成功的响应数据
        :param response_dict:
        :return:
        """

        self.http_mothods_result["result"] = result
        self.handle_response(self.http_mothods_result)
        return


    def __handle_exception(self, e=None):
        """
        异常处理，在header中写入操作结果
        :param e:
        :return:
        """
        api = self.get_api_name()
        errno, errmsg = E_FAILED
        if not e:
            errno, errmsg = E_OK
            #self.write(self.http_mothods_result)
            #return
        elif isinstance(e, BizError):
            errno, errmsg = e.value
        else:
            logging.error(e)

        result = {"api": api, "errno": errno}
        if setting.IS_DEBUG:
            result["errmsg"] = errmsg

        self.add_header("result", json.dumps([result]))

        if e:
            self.http_mothods_result["_result"] = False
            self.http_mothods_result["success"] = False
            self.http_mothods_result["message"] = errmsg

            self.write(self.http_mothods_result)


    def handle_response(self, result_dict):
        """
        处理返回内容，如果是web访问，则返回jsonp内容，否则直接返回处理结果
        # 浏览器请求接口时，一定会有参数"jsonp_callback",  客户端请求时没有。
        :param result_dict:
        :return:
        """

        jsonp_callback = self.request.headers.get("jsonp_callback", "")
        if not jsonp_callback:
            jsonp_callback = self.get_argument("jsonp_callback", "")

        if not jsonp_callback:
            self.write(result_dict)
        else:
            self.write('%s(%s);' % (jsonp_callback, json.dumps(result_dict)))

    def get_api_name(self):
        """
        从request取得请求的api名称
        :return:
        """
        api = self.request.uri
        if api.find("?") > 0:
            api = api[: api.find("?")]
        return api

    def handle_exception(self, e=None):
        """
        开放 异常处理
        :param e:
        :return:
        """
        self.__handle_exception(e)


    def get_current_user(self):
        """

        用户登录验证
        使用 @tornado.web.authenticated进行登录认证
        需要配置login_url, 否则抛出403错误
        :return:
        """
        return self.get_account_id()

    # def set_default_headers(self):
    #     """
    #     @author : Sven
    #     设置X-Xsrftoken响应头
    #     通知前端的请求头上加上 X-Xsrftoken
    #     :return:
    #     """
    #
    #     self.add_header("X-Xsrftoken", self.xsrf_token)
    #     self.add_header("Access-Control-Allow-Origin", "*")
    #     self.add_header("Access-Control-Allow-Methods","POST, HEAD, OPTIONS")
    #     self.add_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, \
    #                    Content-Type, Accept, X-Xsrftoken, result, token,since")


    def write_error(self, status_code, **kwargs):
        """
        http错误处理
        :param status_code:
        :param kwargs:
        :return:
        """
        self.__handle_exception()