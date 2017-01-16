#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import wechatpy


from web.route import route
from web.base import BaseRequestHandler
from common.tools.data import now_timestamp



from common.wechat.wechat_settings import WX_PUBLIC
__author__ = 'raymondlei'

wx = wechatpy.pay.WeChatPay(
    appid=WX_PUBLIC['APP_ID'],
    api_key=WX_PUBLIC['API_KEY'],
    mch_id=WX_PUBLIC['MCH_ID'],
    mch_cert=WX_PUBLIC['MCH_CERT'],
    mch_key=WX_PUBLIC['MCH_KET']
)


@route('/test/wxcoupon')
class WXCouponHandler(BaseRequestHandler):
    """
    代金券接口
    """

    def do_post(self):
        try:

            wxcp = wechatpy.pay.api.coupon.WeChatCoupon

        except Exception as e:
            logging.debug(e+'微信支付，代金券接口异常!')


@route('/test/wxorder')
class WXOrderHandler(BaseRequestHandler):
    """
    订单接口
    """

    wxorder = wechatpy.pay.api.WeChatOrder

    def do_post(self):
        """
        统一下单接口

        :param trade_type:      交易类型，取值如下：JSAPI，NATIVE，APP，WAP
        :param body:            商品描述
        :param total_fee:       总金额，单位分
        :param notify_url:      接收微信支付异步通知回调地址
        :param client_ip:       可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param user_id:         可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no:    可选，商户订单号，默认自动生成
        :param detail:          可选，商品详情
        :param attach:          可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type:        可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start:      可选，订单生成时间，默认为当前时间
        :param time_expire:     可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag:       可选，商品标记，代金券或立减优惠功能的参数
        :param product_id:      可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info:     可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param limit_pay:       可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据
        """

        try:

            body_json = self.get_json_request_body()

            trade_type = body_json.get('trade_type', 'WAP')                       # 这里方便测试选择WAP方式，可通过URL直接访问
            body = body_json.get('body', None)
            total_fee = body_json.get('total_fee', None)
            notify_url = body_json.get('notify_url', None)
            client_ip = body_json.get('client_ip', None)                          # 可选
            user_id = body_json.get('user_id', None)                              # 可选
            out_trade_no = body_json.get('out_trade_no', None)                    # 可选
            detail = body_json.get('detail', None)                                # 可选
            attach = body_json.get('attach', None)                                # 可选
            fee_type = body_json.get('fee_type', 'CNY')                           # 可选
            time_start = body_json.get('time_start', now_timestamp)               # 可选  默认为当前时间
            time_expire = body_json.get('time_expire', None)                      # 可选
            goods_tag = body_json.get('goods_tag', None)                          # 可选
            product_id = body_json.get('product_id', None)                        # 可选
            device_info = body_json.get('device_info', 'WEB')                     # 可选
            limit_pay = body_json.get('limit_pay', None)

            if body_json:

                res = self.wxorder.create(
                    trade_type,
                    body,
                    total_fee,
                    notify_url,
                    client_ip,
                    user_id,
                    out_trade_no,
                    detail,
                    attach,
                    fee_type,
                    time_start,
                    time_expire,
                    goods_tag,
                    product_id,
                    device_info,
                    limit_pay
                    )

                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，统一下单错误!')

        except Exception as e:
            logging.debug(e+str('微信支付,统一下单异常!'))

    def do_get(self):
        """
        查询订单

        :param transaction_id: 微信的订单号，优先使用
        :param out_trade_no: 商户系统内部的订单号，当没提供transaction_id时需要传这个。
        :return: 返回的结果数据
        """
        try:

            transaction_id = self.get_argument('transaction_id', None)
            out_trade_no = self.get_argument('out_trade_no', None)
            if transaction_id and out_trade_no:
                res = self.wxorder.query(transaction_id, out_trade_no)
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，查询订单错误!')

        except Exception as e:
            logging.debug(e+str('微信支付，查询订单异常!'))

@route('/test/wxclorder')
class WXOrderCloseHandler(BaseRequestHandler):
    """
    订单接口
    """

    def do_get(self):
        """
        关闭订单
        :param out_trade_no: 商户系统内部的订单号
        :return: 返回的结果数据
        """
        try:
            wxorder = wechatpy.pay.api.WeChatOrder
            data = {
                'appid': WX_PUBLIC['APP_ID'],                              # 应用ID
                'out_trade_no': self.get_argument('out_trade_no', None)    # 运单号
            }
            if data['out_trade_no']:

                res = wxorder._post('pay/closeorder', data=data)
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，关闭订单错误!')

        except Exception as e:
            logging.debug(e+str('微信支付，关闭订单异常!'))


class WXAPPPayParamHandler(BaseRequestHandler):
    """
    获取APP支付参数
    """

    def do_get(self):
        """

        """



@route('/test/wxrefund')
class WXRefundHandler(BaseRequestHandler):
    """
    退款接口
    """
    wxref = wechatpy.pay.api.refund.WeChatRefund

    def do_post(self):
        """
        申请退款

        :param total_fee: 订单总金额，单位为分
        :param refund_fee: 退款总金额，单位为分
        :param out_refund_no: 商户系统内部的退款单号，商户系统内部唯一，同一退款单号多次请求只退一笔
        :param transaction_id: 可选，微信订单号
        :param out_trade_no: 可选，商户系统内部的订单号，与 transaction_id 二选一
        :param fee_type: 可选，货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param op_user_id: 可选，操作员帐号, 默认为商户号
        :param device_info: 可选，终端设备号
        :return: 返回的结果数据
        """
        try:
            body_json = self.get_json_request_body()
            total_fee = body_json.get('total_fee', None)
            refund_fee = body_json.get('refund_fee', None)
            out_refund_no = body_json.get('out_refund_no', None)
            transaction_id = body_json.get('transaction_id', None)                          # 可选
            out_trade_no = body_json.get('out_trade_no', None)                              # 可选
            fee_type = body_json.get('fee_type', None)                                      # 可选
            op_user_id = body_json.get('op_user_id', None)                                  # 可选
            device_info = body_json.get('device_info', None)                                # 可选

            if body_json:

                res = self.wxref.apply(
                    total_fee,
                    refund_fee,
                    out_refund_no,
                    transaction_id,
                    out_trade_no,
                    fee_type,
                    op_user_id,
                    device_info
                )
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，退款申请错误!')
        except Exception as e:
            logging.debug(e+str('微信支付，退款申请异常!'))



    def do_get(self):
        """
        查询退款

        :param refund_id: 微信退款单号
        :param out_refund_no: 商户退款单号
        :param transaction_id: 微信订单号
        :param out_trade_no: 商户系统内部的订单号
        :param device_info: 可选，终端设备号
        :return: 返回的结果数据
        """
        try:
            refund_id = self.get_argument('refund_id', None)
            out_refund_no = self.get_argument('out_refund_no', None)
            transaction_id = self.get_argument('transaction_id', None)
            out_trade_no = self.get_argument('out_trade_no', None)
            device_info = self.get_argument('device_info', None)
            if refund_id and out_refund_no and transaction_id and out_trade_no:

                res = self.wxref.query(refund_id, out_refund_no, transaction_id, out_trade_no, device_info)
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，退款查询错误!')

        except Exception as e:
            logging.debug(e+str('微信支付，退款查询异常!'))



@route('/test/parseres/(\w+)')
class WXParseResultHandler(BaseRequestHandler):
    """
    解析微信支付结果通知
    """

    def do_get(self, xml):

        try:
            if str(xml):
                res = wx.parse_payment_result(xml)
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，支付结果通知错误!')
        except Exception as e:
            logging.debug(e+str('微信支付，支付结果通知异常！'))

@route('/test/wxtransfer')
class WXTransferHandler(BaseRequestHandler):

    """
    微信支付企业付款接口
    """
    wct = wechatpy.pay.api.WeChatTransfer()

    def do_post(self):

        """
        企业付款接口

        :param user_id: 接受收红包的用户在公众号下的 openid
        :param amount: 付款金额，单位分
        :param desc: 付款说明
        :param client_ip: 可选，调用接口机器的 IP 地址
        :param check_name: 可选，校验用户姓名选项，
                           NO_CHECK：不校验真实姓名,
                           FORCE_CHECK：强校验真实姓名（未实名认证的用户会校验失败，无法转账）,
                           OPTION_CHECK：针对已实名认证的用户才校验真实姓名（未实名认证用户不校验，可以转账成功）,
                           默认为 OPTION_CHECK
        :param real_name: 可选，收款用户真实姓名，
                          如果check_name设置为FORCE_CHECK或OPTION_CHECK，则必填用户真实姓名
        :param out_trade_no: 可选，商户订单号，需保持唯一性，默认自动生成
        :param device_info: 可选，微信支付分配的终端设备号
        :return: 返回的结果信息
        """

        try:

            body_json = self.get_json_request_body()
            user_id =  body_json.get('user_id', None)
            amount = body_json.get('amount', None)
            desc = body_json.get('desc', None)
            client_ip = body_json.get('client_ip', None)
            check_name = body_json.get('check_name', None)
            real_name = body_json.get('real_name', None)
            out_trade_no = body_json.get('out_trade_no', None)
            device_info = body_json.get('device_info', None)

            if user_id and amount and desc:

                res = self.wct.transfer(
                    user_id,
                    amount,
                    desc,
                    client_ip,
                    check_name,
                    real_name,
                    out_trade_no,
                    device_info
                                   )

                if res:

                    self.write_warning('微信支付，企业付款接口错误!')

        except Exception as e:

            logging.debug(e+str('微信支付，企业付款接口异常!'))


    def do_get(self):
        """
        企业付款查询接口

        :param out_trade_no: 商户调用企业付款API时使用的商户订单号
        :return: 返回的结果数据
        """

        try:

            out_trade_no = self.get_argument('out_trade_no', None)

            if out_trade_no:

                res = self.wct.query(out_trade_no)

                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，企业付款查询接口错误!')

        except Exception as e:

            logging.debug(e+str(('微信支付，企业付款查询接口异常!')))

@route('/test/wxjsapi')
class WXJSAPIHandler(BaseRequestHandler):
    """
    公众号网页JSAPI接口
    """
    wxjs = wechatpy.pay.api.WeChatJSAPI

    def do_post(self):
        """
        获取 JSAPI 签名

        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :return: 签名
        """
        try:
            body_json = self.get_json_request_body()

            prepay_id = body_json.get('prepay_id', None)
            timestamp = body_json.get('timestamp', now_timestamp)
            nonce_str = body_json.get('nonce_str', None)
            
            if prepay_id:
                res = self.wxjs.get_jsapi_signature(prepay_id, timestamp, nonce_str)
                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，获取JSAPI签名错误!')
        except Exception as e:
            logging.debug(e+str('微信支付，获取JSAPI签名异常!'))



    def do_get(self):
        """
        获取 JSAPI 参数

        :param prepay_id: 统一下单接口返回的 prepay_id 参数值
        :param timestamp: 可选，时间戳，默认为当前时间戳
        :param nonce_str: 可选，随机字符串，默认自动生成
        :return:
        """

        try:

            prepay_id = self.get_argument('prepay_id', None)
            timestamp = self.get_argument('timestamp', now_timestamp)
            nonce_str = self.get_argument('nonce_str', None)

            if prepay_id:

                res = self.wx_jsapi.get_jsapi_params(prepay_id, timestamp, nonce_str)

                if res:
                    self.write(res)
                else:
                    self.write_warning('微信支付，获取JSAPI参数错误!')

        except Exception as e:
            logging.debug(e+str('微信支付，获取JSAPI参数异常！'))
















