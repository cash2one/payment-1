#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
需要登录的单元测试范例
"""


__author__ = 'swzs'

def test_check_keys(test_instance, data_dict, key_list):
    """
    检查数据是否存在
    """
    if not isinstance(data_dict, dict):
        test_instance.fail('dictionary expected')

    for key in key_list:
        test_instance.assertIn(key, data_dict)


def check_account_data(test_instance, data_dict):
    """
    账户信息
    :param test_instance:
    :param data_dict:
    :return:
    """
    check_data_dict(test_instance, data_dict)
    test_check_keys(
        test_instance,
        data_dict,
        ['_id','name', 'email', 'phone', 'tel', 'address', 'enterprise_validate', 'cre_time', 'upd_time']
    )


def check_data_dict(test_instance, data_dict):
    if not isinstance(data_dict, dict):
        test_instance.fail('dictionary expected')
    return