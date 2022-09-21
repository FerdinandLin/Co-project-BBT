# -*- coding:utf-8 -*-
# @FileName    :camera.py
# @IDE         :PyCharm
# @Time        :2022/9/20 19:40
# @Author      :Lin
# @Desc        :

from picamera2 import Picamera2, Preview
import libcamera
from time import sleep

picam2 = Picamera2()
camera_config = picam2.reate_still_configuration()

def camera_init():
    """摄像头启动初始化,使用预设配置文件"""
    picam2.configure(camera_config)
    picam2.start()
    print('Raspberry Pi摄像头初始化')
    return 0


def camera_preview(show = True):
    """启用预览

    :param show: 预览形式，默认为True
    """
    picam2.stop_preview()
    picam2.start_preview(show)
    print(show, '预览已切换')
    return 0
