# -*- coding:utf-8 -*-
# @FileName    :shoot.py
# @IDE         :PyCharm
# @Time        :2022/10/12 16:00
# @Author      :Lin
# @Desc        :

from PIL import Image, ImageFilter, ImageEnhance
import os
import core.camera as cam


def save(path):
    img = cam.shoot('image')
    img.save(path)
