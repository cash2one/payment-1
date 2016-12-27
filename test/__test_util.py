#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common_db.redis_key import redis_account_online_key, redis_account_simulation_online_key
from common_tools.data import cre_user_token
from common_db.db_utils.redis_db import redis_db

__author__ = 'swzs'


def user_online_sign(user_id, uip, uname):
    """
    模拟用户登陆
    :param user_id:
    :return:
    """
    uid = int(user_id)
    user_key = redis_account_simulation_online_key(uid)
    token = cre_user_token(uid, uip, uname)
    return redis_db.redis_account_online.hset(user_key, token)


def user_online_out(user_id):
    """
    模拟用户登出
    :param user_id:
    :return:
    """
    user_key = redis_account_online_key(user_id)
    return redis_db.redis_user_simulation_online.hdel(user_key, user_id)