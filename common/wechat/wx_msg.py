#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, time
import xml.etree.ElementTree as ET
from wechatpy import parse_message


__author__ = 'raymondlei'


class WXMsg:

    def __init__(self):
        pass

    def author(self, body):

        """
        接收关注/取消关注 事件推送
        :param body:
        :return:
        """

        logging.debug('微信消息回复中心】收到用户消息' + str(body.decode('utf-8')))

        data = ET.fromstring(body)

        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text

        if MsgType == 'event':

            '''接收事件推送'''

            try:

                Event = data.find('Event').text

                if Event == 'subscribe':

                    # 关注事件
                    CreateTime = int(time.time())

                    reply_content = '欢迎关注我的公众号~'

                    out = self.reply_text(FromUserName, ToUserName, CreateTime, reply_content)

                    self.write(out)

            except:
                pass

    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):

        """
        回复文本消息模板
        :param FromUserName:发送方帐号（一个OpenID）
        :param ToUserName:开发者微信号
        :param CreateTime:消息创建时间 （整型）
        :param Content:文本消息内容
        :return:
        """
        textTpl = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>"""

        return textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)


    #**********************************************第三方引用包的一些实现***************************************************

    def parse_msg_xml(self, xml_doc):
        """
        解析XML消息
        :param xml_doc:
        :return:
        """
        try:
            return parse_message(xml_doc)
        except Exception as e:
            logging.debug("第三方库解析XML消息异常"+str(e))

wx_msg = WXMsg()


if __name__ == '__main__':
    pass