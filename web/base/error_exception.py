#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'swzs'


#=============================操作类错误定义====================================
# 操作成功
E_OK = (1, u'操作成功!')
# 操作失败
E_FAILED = (2, u'操作失败!')
# 请求成功
E_SUCCESS_FUL= (3, u'请求成功!')
# 请求失败
E_UNSUCCESS_FUL = (4, u'请求失败!')
# 上传成功
E_UPLOAD = (5, u'上传成功!')
# 上传失败
E_UNUPLOAD = (6, u'上传失败!')
# 登录失败
E_LOGIN = (7, u'登录失败!')
# 用户未登录
E_NOT_LOGIN = (8, u'用户未登录!')



# 验证码错误
E_NOT_CODE = (9, u'手机验证码错误!')
# 邮箱认证错误
E_NOT_MAIL = (10, u'邮箱认证错误!')
# 无效的参数
E_NOT_PARARM = (11, u'无效的参数!')
# 议价初始化错误
E_INIT_ERROR = (12, u'初始化错误!')

# 手机号错误
E_PHONE_NUMBER = (15, u'手机号错误!')
# 邮件地址非法
E_MAIL_ADDRESS = (16, u'邮件地址非法!')
# 激活邮箱失败
E_MAIL_ACTIVATION = (17, u'激活邮箱失败!')
# 用户ID错误
E_ACCOUNT_ID = (18, u'用户ID错误')
# 账户已注册
E_ACCOUNT_REPEAT = (19, u'账户已注册')

#收藏夹
E_FAVORITE_TWICE = (20, u'已在收藏中')

#=============================系统类错误定义=====================================

# 系统错误
S_ERROR = (1001, u'系统错误!')

