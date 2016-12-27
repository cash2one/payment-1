#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
redis列表KEY
"""

__author__ = 'swzs'

def redis_account_token_key(token):
    """
    在线账户
    :param token:
    :return:
    """
    return 'token:%s' % token

def redis_account_online_key(account_id):
    """
    账户在线
    :param account_id
    :return:
    """
    return 'account_online:%s' % account_id


def redis_account_simulation_online_key(account_id):
    """
    模拟账户在线
    :param account_id:
    :return:
    """
    return 'account_simulation_online:%s' % account_id


def redis_order_key(order_id):
    """
    订单缓存
    :param order_id:
    :return:
    """
    return 'order_cache:%s' % order_id


def redis_rate_key(rate_id):
    """
    议价缓存
    :param rate_id:
    :return:
    """
    return 'rate_cache:%s' % rate_id


def redis_phone_code_key(phone):
    """
    6位数的手机验证码
    :param phone:
    :return:
    """
    return 'phone_code_cache:%s' % phone


def redis_email_activation(em_token):
    """
    邮箱激活
    :param em_token:
    :return:
    """
    return 'email_activation_cache:%s' % em_token



def redis_png_checkout():
    """
    图片缓存域
    :return:
    """
    return "png_checkout"