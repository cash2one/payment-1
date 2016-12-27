#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'swzs'

#默认页数
PAGE_SIZE_DEFAULT = 10


#记住一周(秒)
SEVEN_DAY_TIME_OUT = 604800

#记住一天
ONE_DAY_TIME_OUT = 86400

#记住一小时
ONE_HOUR_TIME_OUT = 3600

#验证码超时时间(秒)
CAPTCHA_TIME_OUT = 60

#订单状态
ORDER_APPLY = 1 #申请议价
ORDER_GOING = 2 #议价中
ORDER_WATING = 3 #待完成
# ORDER_COMPLETED = 4 #已完成
ORDER_CLOSE = 5 #已关闭

#发布类型
RELEASE_TYPE_SUPPLY = 0     #供应
RELEASE_TYPE_DEMAND = 1     #需求

#是否拆售
IS_DIVIDE_SALES = True       #拆售
NO_DIVIDE_SALES = False      #默认不拆售

#是否含税
IS_TAX = True                #含税
NO_TAX = False               #默认不含税

#是否需授权
IS_NEGOTIATE = True          #授权
NO_NEGOTIATE = False         #公开

#是否急售
IS_URGENT_SALES = True       #急售
NO_URGENT_SALES = False      #不急

#油品状态
OIL_SHOW = 6                 #显示
OIL_TRANSACTION = 7          #交易中
# OIL_STOCK = 8              #库存
OIL_CLOSE = 9                #关闭

#账户认证情况
APPROVE_NO = 0
APPROVE_GOING = 1
APPROVE_COMPLETED = 2

#急件申请状态
APPLY_NO_DEAL = 0     #未处理
APPLY_HAD_DONE = 1    #已处理
APPLY_HAD_CLOSED = 2  #关闭

#消息小助手状态
INFO_NO_DEAL = 0
INFO_HAD_DONE = 1
INFO_HAD_CLOSED = 2

