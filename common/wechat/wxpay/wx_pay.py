#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    微信
'''

import logging

import wechatpy

from wechatpy.pay import WeChatPay, api

from common.wechat.wechat_settings import WX_PUBLIC

__author__ = 'raymondlei'


class WXPayObj:
    """
    微信支付接口
    """

    def __init__(self):
        self.appid = WX_PUBLIC['APP_ID']            # 微信公众号 appid
        self.api_key = WX_PUBLIC['API_KEY']         # 商户 key
        self.mch_id = WX_PUBLIC['MCH_ID']           # 商户号
        self.sub_mch_id = None                      # 可选，子商户号，受理模式下必填
        self.mch_cert = WX_PUBLIC['MCH_CERT']       # 商户证书路径
        self.mch_key = WX_PUBLIC['MCH_KEY']         # 商户证书私钥路径

    def wx_chat_pay(self):
        """
        微信红包接口
        :return: obj
        """
        try:
            return WeChatPay(self.appid, self.api_key, self.mch_id, self.sub_mch_id, self.mch_cert, self.mch_key)
        except Exception as e:
            logging.debug('微信红包接口异常'+ str(e))

    def wx_coupon(self):
        """
        微信代金券接口
        :return: obj
        """
        try:
            return wechatpy.pay.api.coupon.WeChatCoupon
        except Exception as e:
            logging.debug('微信代金券接口异常'+ str(e))

    def wx_micropay(self):
        """
        微信退款接口
        :return: obj
        """
        try:
            return wechatpy.pay.api.micropay.WeChatMicroPay
        except Exception as e:
            logging.debug('微信退款接口异常'+ str(e))

    def wx_order(self):
        """
        微信订单接口
        :return:
        """
        try:
            return wechatpy.pay.api.order.WeChatOrder
        except Exception as e:
            logging.debug('微信订单接口异常'+ str(e))

    def wx_parse_payment_result(self, xml):
        """
        微信解析支付结果通知
        :param xml:
        :return:
        """
        try:
            return WeChatPay.parse_payment_result(xml)
        except Exception as e:
            logging.debug('微信解析支付结果异常' + str(e))

    def wx_redpack(self):
        """
        微信红包接口
        :return:
        """
        try:
            return wechatpy.pay.api.redpack.WeChatRedpack
        except Exception as e:
            logging.debug('微信红包接口异常' + str(e))

    def wx_refund(self):
        """
        微信刷卡支付接口
        :return:
        """
        try:
            return wechatpy.pay.api.refund.WeChatRefund
        except Exception as e:
            logging.debug('微信刷卡支付接口异常' + str(e))

    def wx_tools(self):
        """
        微信工具类接口
        :return:
        """
        try:
            return wechatpy.pay.api.tools.WeChatTools
        except Exception as e:
            logging.debug('微信工具类接口异常' + str(e))

    def wx_transfer(self):
        """
        微信企业付款接口
        :return:
        """
        try:
            return wechatpy.pay.api.transfer.WeChatTransfer
        except Exception as e:
            logging.debug('微信企业付款接口异常' + str(e))


wx_pay = WXPayObj()
