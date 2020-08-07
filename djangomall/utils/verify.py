# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2020/8/7

"""
生成验证码：
1 准备素材
字体（ttf) 字体内容 颜色 干扰线
2 画验证码
pip install Pillow , random
创建图片
记录文字内容 django session 服务器端 python代码
abcdefg cookie 浏览器端

1 第一次请求，cookie + session 对应关系生成
2 第二次请求，携带了cookie 找到对应的session 【提交表单】
  请求带上验证码参数 与session中的验证码进行比较
3 io文件流
BytesIO
"""
import random

import os

from PIL import Image, ImageDraw
from django.conf import settings
from io import BytesIO

from django.http import HttpResponse


class VerifyCode(object):
    """验证码类"""

    def __init__(self, dj_request):
        self.dj_request = dj_request
        # 验证码长度
        self.code_len = 4
        # 验证码图片尺寸
        self.img_with = 100
        self.img_height = 30

        self.session_key = "verify_code"

    def gen_code(self):
        """生成验证码"""
        # 1 使用随机数生成验证码字符串
        code = self._get_vcode()
        # 2 把验证码存在的session
        self.dj_request.session[self.session_key] = code
        # 3 准备随机元素(背景颜色，验证码颜色 干扰线，)
        font_color = ["black", "brown", "red"]
        # RGB随机背景颜色
        bg_color = (random.randrange(230,255), random.randrange(230,255), random.randrange(230,255))
        font_path = os.path.join(settings.BASE_DIR, "static","font","timesbi.ttf")
        # 创建图片
        im = Image,new("RGB",(self.img_with, self.img_height), bg_color)
        draw = ImageDraw.Draw(im)

        # 画干扰线
        line_color = random.choice(font_color)
        draw.line((0,0 , self.img_with, self.img_height). fill=line_color, width=5)

        buf = BytesIO()
        im.save(buf,"gif")
        return HttpResponse(buf.getvalue(), "image/gif")


    def _get_vcode(self):
        random_str = "ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"
        code_list = random.sample(list(random_str), self.code_len)
        code = "".join(code_list)
        return code

    def validate_code(self, code):
        """验证验证码是否正确"""
        # 1 转变大小写
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, None)
        # if vcode.lower() == code:
        #     return True
        # return False
        return vcode.lower() == code

if __name__ == '__main__':
    client = VerifyCode(None)
    client.gen_code()