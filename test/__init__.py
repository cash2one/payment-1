#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'swzs'

"""
单元测试包
"""
import json
import os
import requests
from tornado.testing import AsyncTestCase
from setting import LOCALITY_HOST, SERVER_PORT
from test.__test_util import user_online_sign, user_online_out

__author__ = 'bjy'


class SimpleTestHandler(AsyncTestCase):
    """
    无需登陆\异步单元测试基类
    """

    BASE_HOST_URL = 'http://%s:%s/v1' % (LOCALITY_HOST, SERVER_PORT)
    HEADERS = {'content-type': 'application/json'}

    @classmethod
    def simulation_user_login(cls, uid, uip, uname):
        """
        模拟用户登录
        :param cls:
        :param uid:
        :return:
        """
        return user_online_sign(uid, uip, uname)

    @classmethod
    def simulation_user_loginout(cls, uid):
        """
        模拟用户登出
        :param cls:
        :return:
        """
        return user_online_out(uid)

    def get_url(self, url):
        """
        获得URL
        :param url:
        :return:
        """
        return '%s%s' % (self.BASE_HOST_URL, url)

    def assertSuccessResponse(self, response):
        """
        断言成功
        :param response:
        :return:
        """
        if isinstance(response, dict):
            json_response = response
        else:
            json_response = response.json()
        self.assertIn("_result", json_response)
        self.assertTrue(json_response['_result'])

    def assertExceptionResponse(self, response, errno=None):
        """
        断言失败
        :param response:
        :param errno:
        :return:
        """
        json_response= json.loads(response.headers.get('_result'))
        self.assertIsInstance(json_response, list)

        self.assertIn("errno", json_response[0])
        if errno is not None:
            self.assertEqual(errno, json_response[0]['errno'])

    def remove_img(self, upload):
        """
        清理测试用上传的文件
        :param upload:
        :return:
        """
        for img in os.listdir(upload):
            img_file = str(os.path.join(upload, img))
            if os.path.exists(img_file):
                os.remove(img_file)


    def file_json(self, url, files):
        """
        post file
        :param url:
        :param files: files = {'file': open('report.xls', 'rb')}
        :return:
        """
        if files:
            get_url = self.get_url(url)
            r = requests.post(get_url, files=files)
        return r.json()

    def post(self, url, data_dict):
        """
        post 请求单元测试基础方法
        :rtype : object
        :param url:
        :param data_dict:
        :return: json
        """
        if url[0] == '/' and isinstance(data_dict, dict):
            get_url = self.get_url(url)
        return requests.post(get_url, json=data_dict)

    def fetch(self, url):
        """
        get 请求单元测试基础方法
        :param url:
        :return json
        """
        if url[0] == '/':
            get_url = self.get_url(url)
        return requests.get(get_url)

    def put(self, url, set_dict=None):
        """
        put 请求单元测试基础方法
        :param url:
        :param set_dict:
        :return:
        """
        if url[0] == '/':
            get_url = self.get_url(url)
        return requests.put(get_url, set_dict)

    def patch(self, url, data_dict):
        """
        patch 请求单元测试基础方法
        :param url:
        :param data:
        :param kwargs:
        :return:
        """
        if url[0] == '/' and data_dict:
            get_url = self.get_url(url)
        return requests.patch(get_url, data_dict)

    def delte(self, url):
        """
        delete 请求单元测试基础方法
        :param url
        :param data_dict
        return json:
        """
        if url[0] == '/':
            get_url = self.get_url(url)
        return requests.delete(get_url)

    def patch_json(self, url, data_dict):
        """
        patch json 请求单元测试基础方法
        :param url:
        :param data_dict:
        :return:
        """
        r = self.patch(url, data_dict)
        if isinstance(r, object):
            return r.json()
        return r.json()

    def fetch_json(self, url):
        """
        fetch json请求单元测试的基础方法
        :param
        :return json
        """
        r = self.fetch(url)
        return r.json()

    def post_json(self, url, data_dict):
        """
        post 请求单元测试单基础方法
        :param url
        :return json
        """
        r = self.post(url, data_dict)

        return r.json()

    def fetch_by_dict(self, url, data_dict):
        """
        带参数的 fetch 请求单元测试单基础方法
        :param url
        :param data_dict
        :return json
        :author qiao
        """
        if url[0] == '/' and data_dict:
            get_url = self.get_url(url)
        return requests.get(get_url, params=data_dict).json()

class SignTestHandler(SimpleTestHandler):
    """
    单元测试基类(需要登陆)
    """

    @classmethod
    def simulsetUpClass(cls, uid):
        """
        登录
        :param uid:
        :return:
        """
        SimpleTestHandler.setUpClass()
        return SimpleTestHandler.simulation_user_login(uid)

    @classmethod
    def tearDownClass(cls, uid):
        """
        登出
        :param uid:
        :return:
        """
        SimpleTestHandler.tearDownClass()
        return cls.simulation_user_loginout(uid)

    def post(self, url, data_dict):
        """
        post 请求单元测试基础方法
        :param url:
        :param data_dict:
        :return: json
        """
        if url[0] == '/' and isinstance(data_dict, dict):
            geturl = self.get_url(url)
        return requests.post(geturl, json=data_dict)

    def fetch(self, url):
        """
        get 请求单元测试基础方法
        :param url:
        :return json
        """
        if url[0] == '/':
            geturl = self.get_url(url)
        return requests.get(geturl)

    def fetch_json(self, url):
        """
        fetch json请求单元测试的基础方法
        :param
        :return json
        """
        r = self.fetch(url)
        return r.json()

    def post_json(self, url, data_dict):
        """
        post 请求单元测试单基础方法
        :param url
        :return json
        """
        r = self.post(url, data_dict)
        return r.json()

    def fetch_by_dict(self,url,data_dict):
        """
        带参数的 fetch 请求单元测试单基础方法
        :param url
        :param data_dict
        :return json
        :author qiao
        """
        if url[0] == '/' and data_dict:
            get_url = self.get_url(url)
        return requests.get(get_url,params=data_dict).json()