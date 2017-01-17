#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
微信公众号支付单元测试类
"""

import os
import requests
import unittest
import tornado
import tornado.testing
import setting
from test.view_v1 import SimpleTestHandler, SignTestHandler

__author__ = 'raymondlei'



class WXReqHandlserTest(SimpleTestHandler):



    def wx_order_test_01(self):
        """
        微信创建订单
        :return:
        """

        res = self.post_json(url='/test/wxorder', data_dict={'trade_type':'JSAPI',})


    def steps(self):
        for name in sorted(dir(self)):
            if name.startswith("step"):
                yield name, getattr(self, name)

    @tornado.testing.gen_test
    def test_steps(self):
        for name, step in self.steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))

if __name__ == '__main__':
    unittest.main()