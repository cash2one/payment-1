#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import uuid
import os

__author__ = 'swzs'


#短信模版ID
SMS_TEMPLATE_ID = 93052    #1是测试模版,生产环境下应该是其他的值

# 运行目录
SERVER_ROOT = app_root = os.path.dirname(__file__)  # 当前项目根路径

#图片存储位置
IMAGE_ROOT = os.sep.join((SERVER_ROOT, "static", "upload"))#'static/upload'

if not os.path.exists(IMAGE_ROOT): #如果不存在目录创建
    os.makedirs(IMAGE_ROOT)

#Cookie base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
COOKIE_SECRET = '1so2yvT6R32/heckKtz3TqNfDhb8g0i5nIoygXLpDJ0='

# 是否debug模式，正式环境中，这里应设置为False
IS_DEBUG = True

# 是否ZIP
IS_ZIP = True

#是否开启防跨站
IS_COOKIE_XSRF = True


SERVER_PORT = 8080

BASE_HOST = '120.76.156.168'#'120.76.156.105'
LOCALITY_HOST = '127.0.0.1'
HOST_NAME = 'localhost'

if IS_DEBUG:
    BASE_HOST = LOCALITY_HOST
    SMS_TEMPLATE_ID = 1



# redis服务器配置
#端口
REDIS_PORT = 6379

#密码
REDIS_DB_PASSWORD = None

#redis配置
REDIS_BASE_HOST = ''
REDIS_BASE_HOSTREDIS_DB_HOST = 'localhost'

REDIS_DB_ZERO = 0
REDIS_DB_ONE = 1
REDIS_DB_TWO = 2
REDIS_DB_THRESS = 3
REDIS_DB_FOUR = 4
REDIS_DB_FIVES = 5

# mongodb配置
MONGO_DB_HOST = ''
MONGO_DB_LOCAL_HOST = 'localhost'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'p2p_mongo_db'

# Mysql配置
MYSQL_DB_HOST = 'localhost'
MYSQL_DB_PROT = '3306'
MYSQL_DB_NAME = 'p2p_db'
MYSQL_DB_USER = 'root'
MYSQL_DB_PASSWD = 'dc123456'


# email配置
ADMIN_EMAIL = ''
ADMIN_EMAIL_PASSWD = ''
EMAIL_HOST = ''
EMAIL_PORT = 25   #这里默认为25