#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
微信设置
'''

__author__ = 'raymondlei'


# ****************************************公众号资料****************************************

WX_PUBLIC = {

    'PUBLIC_Name': 'DCOnline香港城在线',                                      # 公众号名称
    'SIGNATURE': 'http://pay.sozi.it/base/v1/wxsignature',                   # TOKEN 验证
    'APP_ID': 'wx73d63023f7ae2fc3',                                          # 公众平台应用ID
    'APP_SECRET': '5fe62a404cef6a5a69aaa300bda3152c',                        # 公众平台应用秘钥
    'TOKEN': 'wxpayment',                                                    # 公众号Token配置
    'ENCODINGAESKEY': 'dt5gVCFwulGPUL2h7j29cKWPar3SehTnh4wI3iWIixz',         # 消息加密密钥由43位字符组成，可随机修改
    'MCH_ID':'1330855301',                                                   # 微信支付商户ID
    'BUSINESS_SIGN':'1330855301@1330855301',                                 # 商户平台登录帐号
    'BUSINESS_PASWD':'828167',                                               # 商户平台登录密码
    'API_KEY':'667NXKL1fSvkgjcka9umlpjh4n7JMayu',                            # 商户KEY
    'MCH_CERT': '../common/wechat/cert/',                                    # 商户证书路径
    'MCH_KET':'../common/wechat/cert/'                                       # 商户私钥路径

}

# ****************************************企业号****************************************


# 微信请求基础URL
WX_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'





#****************************************APP支付*********************************************************




#****************************************公众号支付*******************************************************




#****************************************企业号支付*******************************************************

WX_ENT = {
    'TOKEN':'wxpayment',
    'ENCODING_AESKEY':'',
    'CORP_ID':'CorpId'
}










