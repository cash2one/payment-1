#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'swzs'


class Route:

    def __init__(self, prefix=""):
        self.handlers = []
        self._prefix = prefix

    def __call__(self, url, **kwds):
        """
        #这里用 __call__方法用于实例自身的调用，以达到()调用的效果，结合装饰器的原理一起使用
        :param url:
        :param kwds:
        :return:
        """

        def _(cls):
            """
            这里结合面向对象初始化的原理，在当前装饰器被调用的时候追加版本号和url以及类名，还有参数的键值对
            :param cls:当前类名
            :return:
            """
            self.handlers.append((self._prefix + url, cls, kwds))
            return cls

        return _


'''
第一部分为主版本号，第二部分为次版本号，第三部分为修订版，第四部分为日期版本号加希腊字母版本号，希腊字母版本号共有五种，第六部分为语言的版本
分别为base(开发版本)、alpha( 内部测试版)、beta(外部测试版) 、demo(演示版) 、 release（最终释放版）
'''

route = Route(prefix='/base/v1')
