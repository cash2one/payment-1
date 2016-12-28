#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, hashlib, re, json, logging, logging.config, io, random, time, datetime

from bson.objectid import ObjectId

import setting

"""
公共工具类实例
"""

__author__ = 'swzs'


def number_code():
    """
    生成随机的6位数字验证码
    :return:
    """
    number = '0123456789'
    return str(''.join(random.sample(number[0:10],6)))


def cre_user_token(uid, uname):
    """
    生成用户TOKEN,sha1加密
    :param uid:     用户ID
    :param uname:   用户名
    :param nowtime: unix时间戳
    :return:
    """
    result = '%s%s%s' % (uid, uname, time.time())
    return hashlib.sha1(result.encode("utf8")).hexdigest()


def email_token(email):
    """
    生成激活邮箱用的Token
    :param email:
    :param account:
    :param phone:
    :return:
    """
    result = '%s%s%s' % (email, '#', time.time())
    return hashlib.sha1(result.encode("utf8")).hexdigest()


def new_object_id():
    """
    生成一个object id
    :return:
    """
    return str(ObjectId())


def transform_object_id(oid):
    """
    把str类型的id转换成Mongdb主键的ObjectId或者== 互相转换
    :param oid:
    :return:
    """
    if isinstance(oid, ObjectId):
        oid = str(oid)
    else:
        oid = ObjectId(oid)
    return oid

def time_to_object_id(timestamps):
    """
    时间戳转化为ObjectId
    :param timestamps:  当前unix时间戳（单位为秒）
    :return:
    """
    return ObjectId.from_datetime(int(timestamps))

def now_timestamp():
    """
    当前unix时间戳（单位为秒）
    :return:
    """
    return int(time.time())


def now_timemilli():
    """
    当前时间戳（单位为毫秒）
    :return:
    """
    return long(time.time() * 1000)

def md5(key):
    """
    生成MD5加密字符串
    :param key:
    :return:
    """
    return hashlib.md5(key.encode("utf8")).hexdigest()


def init_log(default_path='common/logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    初始化log
    :param default_path , default_level , env_key
    @desc : 參考logging的實現 http://www.iplaypython.com/code/c245.html
    @desc : 每个 Python 程序员都要知道的日志实践 http://python.jobbole.com/81666/
    """

    path = default_path
    value = os.getenv(env_key, None)

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        if setting.IS_DEBUG:  # 判定系統狀態,把日誌同時輸出到屏幕和文件
            config['root']['level'] = "DEBUG"
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    return

def check_phone(phone=None):
    """
    检查 phone 是否合法
    @desc : 最全的常用正则表达式大全 http://blog.jobbole.com/96052/
    """
    if phone and (len(phone) == 11):
        if re.match(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$", phone):
            return True
        else:
            return False

def check_mail(mail=None):
    """
    检查 mail 是否合法
    @desc : 最全的常用正则表达式大全 http://blog.jobbole.com/96052/
    """
    if mail and (len(mail) > 5):
        if re.match(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", mail):
            return True
        else:
            return False

def send_code(phone=None, code=None):
    """
    发送验证码
    :param phone 手机号码 code 验证码
    """
    from common.sms.send_msm_sdk.SendTemplateSMS import sendTemplateSMS
    if phone.isdigit() and isinstance(code, str):
        if 1 == sendTemplateSMS(phone.encode('utf-8'), [code,'1'], getattr(setting, "SMS_TEMPLATE_ID", 1) ):
            return True
    else:
        return False

# TODO
def send_msm(phone=None, context=None):
    """
    发送消息
    :param phone 手机号码 context 内容
    """
    return False
    # from common_tools.send_msm_sdk.SendTemplateSMS import sendTemplateSMS
    # if phone.isdigit() and isinstance(context, str):
    #     if 1 == sendTemplateSMS(phone.encode('utf-8'), {'1', context}, 2):
    #         return True
    # else:
    #     return False


def save_upload_file(body, ext, prefix = ""):
    """
    保存上传文件
    :param body: #文件体
    :param ext: #文件扩展名
    :param prefix: #命名前缀
    :return:
    file_name
    """
    from setting import IMAGE_ROOT

    file_name = ".".join(("_".join((prefix, hashlib.md5(body).hexdigest())), ext))
    full_file_name = os.sep.join((IMAGE_ROOT, file_name))

    #如果存在,直接返回
    if os.path.isfile(full_file_name):
        return file_name

    with open(full_file_name, "wd") as f:
        f.write(body)
        f.flush()

    return file_name


def timestamp_from_now(day = 0):
    """
    返回此刻前n天的时间戳
    :param day:
    :return:
     (day_age, now_datetime)
    """

    now_datetime = datetime.datetime.now()
    now_ts = time.mktime(now_datetime.timetuple())

    if day is 0:
        return now_ts, now_ts
    else:
        day_ago = now_datetime - datetime.timedelta(day=day)
        return time.mktime(day_ago.timetuple()), now_ts


def timestamp_from_today(day = 0):
    """
    返回今天此刻的时间戳,及当天前n天的时间戳
    :param day:
    :return:
    """
    now_datetime = datetime.datetime.now()
    #now_ts = time.mktime(now_datetime.timetuple())
    now_today = now_datetime.date()
    now_tomorow = now_today + datetime.timedelta(1)
    if day is 0: #当天的时间戳,及此刻时间戳
        return time.mktime(now_today.timetuple()), time.mktime(now_tomorow.timetuple())
    else:
        day_ago = now_today - datetime.timedelta(day)
        return time.mktime(day_ago.timetuple()), time.mktime(now_tomorow.timetuple())

def upload_path(img_file_name):
    """
    图片路径
    :param img_file_name:
    :return:
    """
    return "/".join(("upload", img_file_name))


def gen_chcekout_png():
    from PIL import Image
    from io import BytesIO
    imglen = 4

    base = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z')

    code = ""
    checkout_png_path = os.path.dirname(__file__)
    checkout_png = Image.open(os.sep.join((checkout_png_path, "checkout.png")))
    code_img = Image.new("RGBA", (19*imglen, 25))

    #根据长度截取图片,并黏贴到code_img
    for x in range(imglen):
        ran = random.randint(0, 35)
        #添加随机生成的code在base元组中的字符
        code = ''.join((code, base[ran]))
        #img_s 随机截取图片，并在（-45,45）度之间随机旋转，在粘贴上codeimg
        char_img = checkout_png.crop((ran*19, 0, (ran+1)*19, 20))
        char_img = char_img.rotate(random.randint(-45, 45))
        code_img.paste(char_img, (x*19,2))


    #保存于字符流，打印给浏览器
    out = BytesIO()
    code_img.save(out, "png")
    return code, out.getvalue()


def gen_chcekout_jpeg():
    from PIL import Image, ImageFilter, ImageDraw, ImageFont
    from io import BytesIO
    import string

    imglen = 4
    all_letters = "".join((string.digits, string.letters))
    code = "".join(random.sample(all_letters, imglen))
    width, height = 30 * imglen, 25

    code_img = Image.new('RGB', (width, height), (180, 180, 180))
    checkout_font_path = os.path.dirname(__file__)
    logging.info("ttf:%s"%checkout_font_path)
    img_font = ImageFont.FreeTypeFont(os.sep.join((checkout_font_path, "MONACO.TTF")), 24)
    img_draw = ImageDraw.Draw(code_img)

    random_color = lambda :(random.randint(30, 100), random.randint(30, 100), random.randint(30, 100))
    random_point = lambda :(random.randint(0,width),random.randint(0,height))

    #把字符放在图片上
    map(lambda t: img_draw.text((30 * t + 10, 0), code[t], font=img_font, fill=random_color()), xrange(0, imglen))

    #填充噪点
    map(lambda x: img_draw.point((random.randint(0, width), random.randint(0, height)), fill=random_color()), xrange(300, 400))


    # 添加直线
    line_num = random.randint(5,15) #干扰线数量
    map(lambda x: img_draw.line([random_point(), random_point()], random_color()), xrange(0, line_num))

    # 模糊处理
    # code_img = code_img.filter(ImageFilter.BLUR)

    out = BytesIO()
    code_img.save(out, "jpeg")
    return code, out.getvalue()





if __name__ == "__main__":

    #print timestamp_from_today()[0], timestamp_from_today()[1]
    print gen_chcekout_jpeg()