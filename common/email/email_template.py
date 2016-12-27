#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
邮件通知模板
"""

import time

__author__ = 'swzs'
__update_by__ = "sven"

#email_content_template
"""
<html>
              <body>
                <h2>能商行账号激活!<h2>
                <p>
                   您好！您于 {0}注册了能商行账号，请在12小时内点击以下链接，激活该账号：<br>
                   <a href='{1}'><input type='button' value='点击激活'></a> <br>
                   或者 复制以下连接到地址栏打开 {1}
                </p>
                <p>
                   ：提示
                   若您长时间未收到激活邮件，请检查您的垃圾箱或广告箱，邮件有可能被误认为垃圾或广告邮件。
                   如确认无法找到您的激活邮件，可在账户中重新发送激活邮件</a>。
                </p>
              </body>
            </html>

"""

EMAIL_CONTENT_TEMPLATE = """
 <table cellpadding="0" cellspacing="0" border="0" width="640" style="margin:0 auto;color:#555; font:16px/26px '微软雅黑','宋体',Arail; ">
   <tbody>
    <tr>
     <td style="height:62px; background-color:#FF6600; padding:10px 0 0 10px; TEXT-ALIGN: center;"> 能商行账号激活!</td>
    </tr>
    <tr style="background-color:#fff;">
     <td style="padding:10px 38px;">
      <div style="margin:20px 0;">
       <div style="MARGIN-BOTTOM: 10px; HEIGHT: 30px; BORDER-BOTTOM: #e6e6e6 1px solid; TEXT-ALIGN: right; MARGIN-TOP: 10px">
        <span style="FONT-SIZE: 10pt; COLOR: #c0c0c0"></span>
       </div>
       您好！您于 {0}注册了能商行账号，请在12小时内点击以下链接，激活该账号：<br>
        <a href='{1}'><input type='button' value='点击激活'></a> <br>
        或者<br>
        复制以下连接到地址栏打开 {1}

       <div style="height:190px;margin:20px auto 20px auto;width:550px;">
       提示<br>
       若您长时间未收到激活邮件，请检查您的垃圾箱或广告箱，邮件有可能被误认为垃圾或广告邮件。
       <br>
       如确认无法找到您的激活邮件，可在账户中重新发送激活邮件

       </div>
      </div></td>
    </tr>
   </tbody>
  </table>
"""

#EMAIL_CONTENT_TEMPLATE = EMAIL_CONTENT_TEMPLATE.lstrip().rstrip()

def activation_template(activation_url):

    """
    邮箱账户激活模板
    :param activation_url: 邮箱激活
    :param reset_url: 重新发送
    :return:
    """

    ISOTIMEFORMAT = '%Y-%m-%d %X'
    #account_activation = ''''''.format(time.strftime(ISOTIMEFORMAT, time.localtime()), activation_url)


    return EMAIL_CONTENT_TEMPLATE.format(time.strftime(ISOTIMEFORMAT, time.localtime()), activation_url)








