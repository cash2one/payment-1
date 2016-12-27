#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setting import REDIS_BASE_HOST, REDIS_PORT, REDIS_DB_PASSWORD, REDIS_DB_ONE, REDIS_DB_TWO, REDIS_DB_ZERO, \
    REDIS_DB_THRESS, REDIS_DB_FOUR, REDIS_DB_FIVES
import redis


"""
Redis工具类
"""

__author__ = 'swzs'


class RedisUtilsHandler:

    def __init__(self):
        self._open_rate_cache = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_ZERO, password=REDIS_DB_PASSWORD)
        self._account_order_cache = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_ONE, password=REDIS_DB_PASSWORD)
        self._account_online_cache = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_TWO, password=REDIS_DB_PASSWORD)
        self._phone_code_cache = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_THRESS, password=REDIS_DB_PASSWORD)
        self._email_activation = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_FOUR, password=REDIS_DB_PASSWORD)
        #图片验证码缓存
        self._png_checkout = redis.StrictRedis(host=REDIS_BASE_HOST, port=REDIS_PORT, db=REDIS_DB_FIVES, password=REDIS_DB_PASSWORD)



    def exists(self, key):
        """
        检查key是否存在
        :param key:
        :return:
        """
        return self._phone_code_cache.exists(key)

    @property
    def redis_phone_code(self):
        """
        手机验证码
        :return:
        """
        return self._phone_code_cache

    @property
    def redis_email_activation(self):
        """
        邮箱激活码
        :return:
        """
        return self._email_activation

    @property
    def redis_user_simulation_online(self):
        """
        账户在线模拟
        :return:
        """
        return self._account_online_cache

    @property
    def redis_account_online(self):
        """
        账户在线
        :return:
        """
        return self._account_online_cache

    @property
    def redis_account_order_cache(self):
        """
        账户交易订单
        :return:
        """
        return self._account_order_cache

    @property
    def redis_account_open_rate(self):
        """
        账户交易记录
        :return:
        """
        return self._open_rate_cache

    @property
    def redis_png_checkout(self):
        """
        图片验证码缓存记录
        :return:
        """
        return self._png_checkout

redis_db = RedisUtilsHandler()