#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from web.route import route
from web.base import BaseRequestHandler

#微信第三方库

from wechatpy.client import WeChatClient

#内部程序
from common.wechat.wechat_settings import WX_PUBLIC
from common.wechat.wx_token import token_cache

__author__ = 'raymondlei'



@route('/wxaccesstoken')
class WXAccessTokenHandler(BaseRequestHandler):

    """
    获取微信的ACCESS_TOKEN
    """

    # TODO
    def do_get(self):

        try:

            token_timeout = 7000 * 1000  # token过期时间
            wx_client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'], timeout=token_timeout)
            access_token = wx_client.fetch_access_token()

            if access_token:
                # 第三方库的方式拿AccessToken
                self.write(access_token)
            else:
                #自己实现的方式从Redis拿AccessToken缓存
                self.write(token_cache.get_cache(token_cache.KEY_ACCESS_TOKEN))

        except Exception as e:

            self.write_warning('微信回调AccessToken异常'+ str(e))


@route('/wxuser')
class WXUserInfoHandler(BaseRequestHandler):

    """
    用户基本信息接口
    """

    def do_get(self):
        """
        获取用户的基本信息
        参考：http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        :return:
        """
        try:

            opid = self.get_argument('openid', None)

            if opid:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                user = client.user.get(opid)

                if user:
                    self.write(user)
                else:
                    logging.debug('微信获取用户基本信息失败!')

        except Exception as e:

            self.write_warning('微信获取用户信息异常'+ str(e))



    def do_post(self):

        """
        获取用户信息列表,最多支持一次拉取100条。
        参考:http://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
        :return: user_info_list
        """

        try:

            body = self.get_json_request_body()
            ulist = body.get('user_list', None)  #用户id列表

            if isinstance(ulist, list):

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                users = client.user.get_batch(ulist)

                if users:
                    self.write(users)
                else:
                    logging.debug('微信获取用户信息列表失败!')

        except Exception as e:

                self.write_warning('微信获取用户信息列表异常'+ str(e))


@route('/wxfollowers')
class WXFollowersHandler(BaseRequestHandler):

    """
    获取关注者列表
    参考 http://mp.weixin.qq.com/wiki/3/17e6919a39c1c53555185907acf70093.html
    """

    def do_get(self):

        try:

            client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
            followers = client.user.get_followers()

            if followers:
                self.write(followers)
            else:
                logging.debug('微信获取关注者列表失败!')

        except Exception as e:

            self.write_warning('微信获取关注者列表异常'+ str(e))


@route('/wxupdate/remark')
class WXUpdateRemarkHandler(BaseRequestHandler):

    """
    设置用户备注名
    """

    def do_post(self):

        try:

            body = self.get_json_request_body()
            openid = body.get('openid', None)
            remark = body.get('remark', None)

            if openid and remark:
                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                res = client.user.update_remark(openid, remark)
                if res:
                    self.write(res)
                else:
                    logging.debug('微信设置用户备注名失败!')

        except Exception as e:

            self.write_warning('微信设置用户备注名异常'+ str(e))


@route('/wxgroupid')
class WXGroupIDHandler(BaseRequestHandler):

    """
    获取用户所在分组 ID
    """

    def do_post(self):

        try:

            body = self.get_json_request_body()
            opid = body.get('openid', None)  #用户id列表

            if opid:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                group_id = client.user.get_group_id(opid)

                if group_id:
                    self.write(group_id)
                else:
                    logging.debug('微信获取用户分组ID失败!')

        except Exception as e:

            self.write_warning('微信获取用户分组ID异常' + str(e))


@route('/wxgroup')
class WXGroupHandler(BaseRequestHandler):

    """
    用户分组创建、查询用户分组
    """

    def do_post(self):
        """
        创建用户分组
        参考 http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html
        :return:
        """

        try:

            body = self.get_json_request_body()
            group_name = body.get('group_name', None)  #用户分组名称

            if group_name:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                res = client.group.create(group_name)

                if res:
                    self.write(res)
                else:
                    logging.debug('微信创建用户分组失败!')

        except Exception as e:

            self.write_warning('微信创建用户分组异常'+ str(e))

    def do_get(self):

        """
        查询所有分组或查询用户所在分组 ID
        参考 http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html
        """

        try:

            opid = self.get_argument('openid', None)


            client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
            group = client.group.get(opid)

            if group:
                self.write(group)
            else:
                logging.debug('微信查询所有分组或查询用户所在分组 ID失败!')

        except Exception as e:

            self.write_warning('微信查询所有分组或查询用户所在分组 ID异常'+str(e))


@route('/wxgroup/remove')
class WXGroupRemoveHandler(BaseRequestHandler):

    """
    用户分组删除
    """

    def do_post(self):
        """
        删除分组
        参考 http://mp.weixin.qq.com/wiki/0/56d992c605a97245eb7e617854b169fc.html
        :return:
        """

        try:

            body = self.get_json_request_body()
            group_id = body.get('group_id', None)  #用户分组名称

            if group_id:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                res = client.group.delete(group_id)

                if res:
                    self.write(res)
                else:
                    logging.debug('微信删除用户分组失败!')

        except Exception as e:

            self.write_warning('微信删除用户分组异常'+ str(e))


@route('/wxgroup/move')
class WXGroupMemberMoveHandler(BaseRequestHandler):

    """
    移动用户分组
    """

    def post(self):

        """
        移动用户分组
        :return:
        """

        try:

            body = self.get_json_request_body()
            group_id = body.get('group_id', None)  #分组ID 可以是单个或者列表，为列表时为批量移动用户分组
            open_id = body.get('open_id', None)  #用户ID

            if group_id and open_id:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                res = client.group.move_user(open_id, group_id)

                if res:
                    self.write(res)
                else:
                    logging.debug('微信移动用户分组失败!')

        except Exception as e:

            self.write_warning('微信移动用户分组异常'+ str(e))

@route('/wxgroup/modify')
class WXGroupModifyHandler(BaseRequestHandler):

    """
    修改分组名
    """

    def do_post(self):

        try:
            body = self.get_json_request_body()
            group_id = body.get('group_id', None)  #分组ID
            group_name = body.get('group_name', None) #分组名

            if group_id and group_name:

                client = WeChatClient(WX_PUBLIC['APP_ID'], WX_PUBLIC['APP_SECRET'])
                res = client.group.update(group_id, group_name)

                if res:
                    self.write(res)
                else:
                    logging.debug('微信修改分组名失败!')

        except Exception as e:

            self.write_warning('微信修改分组名异常' + str(e))