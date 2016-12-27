#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
邮件组件
"""

import logging, time, sys
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from setting import ADMIN_EMAIL, ADMIN_EMAIL_PASSWD,EMAIL_HOST,EMAIL_PORT

__author__ = 'swzs'

class ErmBankEmailHandler:

    def __init__(self):
        pass

    def account_activation(self, user_email, sub_title, html):
        """
        发送邮件激活账户
        :param user_email:
        :param url:
        :return:
        """
        admin_email = ADMIN_EMAIL
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sub_title
        msg['From'] = admin_email
        msg['To'] = user_email

        part = MIMEText(html, 'html', 'UTF-8')
        msg.attach(part)
        try:
            s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            s.login(msg['From'], ADMIN_EMAIL_PASSWD)
            s.sendmail(admin_email, user_email, msg.as_string())
            s.quit()
        except Exception, e:
            logging.exception('Catch an exception.')
            print '-' * 10
            logging.warning('Catch an exception.', exc_info=True)
            print e
            return False

        return True




send_email = ErmBankEmailHandler()