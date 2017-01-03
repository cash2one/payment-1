#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
微信设置
'''

__author__ = 'raymondlei'


# 公众号资料

WX_PUBLIC = {
    'Publick_Name': 'DCOnline香港城在线',                                      # 公众号名称
    'Signature': 'http://pay.sozi.it/base/v1/wxsignature',                   # TOKEN 验证
    'APP_ID': 'wx73d63023f7ae2fc3',                                          # 公众平台应用ID
    'APP_SECRET': '5fe62a404cef6a5a69aaa300bda3152c',                        # 公众平台应用秘钥
    'TOKEN': 'wxpayment',                                                    # 公众号Token配置
    'ENCODINGAESKEY': 'EMSd6makjA0GRMVen6zw1lqI33FJ6geB4TbugSRAFEB'          # 消息加密密钥由43位字符组成，可随机修改

}


# 微信请求回调URL
WX_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

#
BASE_ID = 'gh_e558308e3180'



#****************************************APP支付*********************************************************




#****************************************公众号支付*******************************************************





# 微信支付商户ID
WX_PUBLIC_PAY_BUSSINESS_ID = '1330855301'

# 商户平台登录帐号
WX_PUBLIC_PAY_SIGN = '1330855301@1330855301'

# 商户平台登录密码
WX_PUBLIC_PAY_PASWD = '828167'

