#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    支付宝
'''

from tornado import gen
from tornado import web

from web.base import BaseRequestHandler
from common.alipay import pay_settings, alipay_core

__author__ = 'raymondlei'


# 服务器地址
HOST = ''

class MakePaymentInfo(BaseRequestHandler):
    """
    构造一个支付请求
    """

    @gen.conroutine
    def do_get(self, order_id):
        '''
        这里是客户端请求服务端来获取提交给支付宝的支付请求， 因为私钥放在客户端来签名的话，可能会遭遇破解，所以构造了这个服务端用来签名的方法
        '''
        self.set_status(200)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        total_fee = 0.01  #这里讲金额设为1分钱，方便测试
        body = ''
        payment_info = self.make_payment_info(
            out_trade_no=order_id,
            subject=order_id,
            total_fee=total_fee,
            body=body)

        res = alipay_core.make_payment_request(payment_info)
        self.write({'status': pay_settings.ALIPAY_STATUS_SUCCESS, 'res': res})


    def make_payment_info(self, out_trade_no=None, subject=None, total_fee=None, body=None):

        order_info = {'partner': '%s' % (pay_settings.ALIPAY_PARTNER_ID),
                      'service': 'mobile.securitypay.pay',
                      '_input_charset': 'utf-8',
                      'notify_url': 'http://%s/callback' % (HOST),

                      #业务参数
                      'out_trade_no': None,
                      'paymnet_type': "1",
                      'subject': None,
                      'seller_id': pay_settings.ALIPAY_ACCOUNT,
                      'total_fee': 0,
                      'body': None
        }

        order_info['out_trade_no'] = '%s' % (out_trade_no)
        order_info['subject'] = '%s' % (subject)
        if total_fee <= 0.0:
            total_fee = 0.01
        order_info['total_fee'] = total_fee
        order_info['body'] = 'hsh_shop'
        return order_info


class PaymentCallBack(web.RequestHandler):
    '''
    阿里支付回调
    '''

    '''
    WAIT_BUY
    body=商品描述&buyer_email=ma.hongwei@foxmail.com&buyer_id=2088702056383644&discount=0.00&gmt_create=2015-07-10 18:06:54&is_total_fee_adjust=Y&notify_id=cf579a7403c6bdc806ccb49101510aa05k&notify_time=2015-07-10 18:06:54&notify_type=trade_status_sync&out_trade_no=PRH0BL7A6QLCSUO&payment_type=1&price=0.01&quantity=1&seller_email=xiaowenwen@7500.com.cn&seller_id=2088021072549071&sign=Lp3JJj4WpR1BggPiC/O0IPGGeIc5xxPLhA7ICvEYElaEv820Ju8GeFXKjepvIlgWa76lMMGW99BPW0HkmqvPRE1thJevKNHQ+KQTIXpw5iKaoXbAXeURrs4LUK6CTIQBpX0fAjfZ4EMAHnx31fgRnJbuuWCOTJ8MLgjLvDmJs9M=&sign_type=RSA&subject=商品测试&total_fee=0.01&trade_no=2015071000001000640055508270&trade_status=WAIT_BUYER_PAY&use_coupon=N
    PAYSUCCESS
    body=商品描述&buyer_email=ma.hongwei@foxmail.com&buyer_id=2088702056383644&discount=0.00&gmt_create=2015-07-10 18:06:54&gmt_payment=2015-07-10 18:06:55&is_total_fee_adjust=N&notify_id=f00d4988288e8e4af8bff37f4b0e365b5k&notify_time=2015-07-10 18:06:55&notify_type=trade_status_sync&out_trade_no=PRH0BL7A6QLCSUO&payment_type=1&price=0.01&quantity=1&seller_email=xiaowenwen@7500.com.cn&seller_id=2088021072549071&sign=CfTvBdJ6blsg0BjDLq51eJn073VkVkoK79kTFOURuN4Av48lvJxN4S4lqm+sRW6xA7AlKBm/pNKqz0eRT1jzFvaG8Nd4C2vMKYzzQ/CrTkDym74od+q04Sdp2X+xB5fKfqeOy3qyFJgpXX1WT7npXjWqAxmT80ZTQiykoufWnNo=&sign_type=RSA&subject=商品测试&total_fee=0.01&trade_no=2015071000001000640055508270&trade_status=TRADE_SUCCESS&use_coupon=N
    '''

    #这里需要做3件事情
    #1验证平台签名
    #2去阿里验证回调信息是否真实
    #3执行业务逻辑，回调订单状态

    @gen.coroutine
    def do_post(self):
        args = self.request.arguments
        for k, v in args.items():
            args[k] = v[0]

        check_sign = self.params_to_query(args)
        params = self.query_to_dict(check_sign)
        sign = params['sign']
        params = self.params_filter(params)
        message = self.params_to_query(params,quotes=False,reverse=False) #获取到要验证签名的串
        check_res = self.check_ali_sign(message,sign)  #验签

        if check_res == False:
            self.write("fail")
            return

        #这里是去访问支付宝来验证订单是否正常
        res = alipay_core.verify_from_gateway({'partner': pay_settings.ALIPAY_PARTNER_ID, 'notify_id': params['notify_id']})
        if res == False:
            self.write('fail')
            return

        trade_status = params['trade_status']
        order_id = params['out_trade_no']  #你自己构建订单时候的订单ID
        alipay_order = params['trade_no']  #支付宝的订单号码
        total_fee = params['total_fee']  #支付总额

        '''
        下面是处理付款完成的逻辑
        '''
        if trade_status == 'TRADE_SUCCESS':  #交易成功
            #TODO:这里来做订单付款后的操作
            self.write('交易成功!')
            return
        if trade_status == 'TRADE_FINISHED':  # 交易完成
            self.write('交易成功!')
            return

        if trade_status == 'WAIT_BUYER_PAY':  # 等待买家付款

            self.write('等待买家付款')
            return
        if trade_status == 'TRADE_CLOSED':     #交易关闭，退款会回调这里
            self.write('交易关闭')