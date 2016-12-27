#-*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

import pickle

#主帐号
# accountSid= 'aaf98f895069246a0150697c43990096';
accountSid= '8a216da854ff8dcc0155095d898d0dda';

#主帐号Token
# accountToken= 'bdd3762a43e445498c713077c28924c9';
accountToken= '737b039b78c549eea0bd03f2cbb62897';

#应用Id
# appId='8a48b5515147eb6d01514cdee0e60ad5';
appId='8a216da854ff8dcc0155095d89ec0de0';

#请求地址，格式如下，不需要写http://
serverIP='sandboxapp.cloopen.com';

#请求端口
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

def sendTemplateSMS(to,datas,tempId):
    # 发送模板短信
    # @param to 手机号码
    # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
    # @param $tempId 模板Id
    # 初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to,datas,tempId)
    # output = open('data.pkl', 'wb')
    # pickle.dump(result, output)
    # pkl_file = open('data.pkl', 'rb')
    # result = pickle.load(pkl_file)
    # print type(result)
    #print int(result['statusCode'])

    #if int(result["statusCode"]) is 0:
    #    return True
    #else:
    #    return False

    """
    #响应1
    属性	            类型	        约束	        说明
    statusCode     String       必选        请求状态码，取值000000（成功）
    smsMessageSid  String	    必选	        短信唯一标识符
    dateCreated    String	    必选	        短信的创建时间


    #响应2
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Response>
            <statusCode>113302</statusCode>
            <statusMsg>【流量】您正在使用云通讯测试模板且短信接收者不是注册的测试号码</statusMsg>
        </Response>

    #响应3
        return {'172001':'网络错误'}
    """
    try:
        status_code = int(result["statusCode"])
    except:
        status_code = -1

    if status_code is 0:
        return True
    else:
        return False



# sendTemplateSMS(u'18374729937',{'asdas','1'},1)
