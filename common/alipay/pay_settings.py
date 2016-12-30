#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    支付对接配置
'''

__author__ = 'raymondlei'


#================alipay================支付宝

# 加密方式
ALIPAY_SIGN_TYPE = 'SHA-1'

# alipay公钥
ALIPAY_RSA_PUBLIC = '''-----BEGIN PUBLIC KEY-----

    -----END PUBLIC KEY-----'''

# 商户私钥
ALIPAY_RSA_PRIVATE = '''-----BEGIN RSA PRIVATE KEY-----

-----END RSA PRIVATE KEY-----'''

# 商户公钥
ALIPAY_RSA_PUBLIC = '''-----BEGIN PUBLIC KEY-----

-----END PUBLIC KEY-----'''

# 支付宝后台合作商ID
ALIPAY_PARTNER_ID = 123456

# 商家的支付宝KEY
ALIPAY_KEY = ''

# 商家的支付宝邮箱
ALIPAY_ACCOUNT = ''


#构造订单信息

ALIPAY_STATUS_SUCCESS = 0                   #成功
ALIPAY_STATUS_PAYED = 1                     #订单已支付
ALIPAY_STAUTS_ORDER_NOT_EXTED = 2           #订单不存在
ALIPAY_STATUS_ORDER_REFUND = 3              #订单已退款
ALIPAY_STATUS_ORDER_STATUS_ERROR = 4        #订单状态错误


# 构造交易信息

ALIPAY_TRADE_SUCCESS = 'TRADE_SUCCESS'      #交易成功
ALIPAY_TRADE_FINISHED = 'TRADE_FINISHED'    #交易完成
ALIPAY_WAIT_BUYER_PAY = 'WAIT_BUYER_PAY'    #等待买家付款
ALIPAY_TRADE_CLOSED = 'TRADE_CLOSED'        #交易关闭




