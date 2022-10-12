# -*- coding:utf-8 -*-
# @FileName    :camera.py
# @IDE         :PyCharm
# @Time        :2022/9/20 19:40
# @Author      :Lin
# @Desc        :

from picamera2 import Picamera2, Preview
import libcamera
from warnings import warn
from time import sleep
import numpy as np

import configparser
config = configparser.ConfigParser()
if __name__ == '__main__':
    confpath = '../conf/config.ini'
else:
    confpath = './conf/config.ini'

config.read(confpath, encoding='utf-8')

picam2 = Picamera2()
# raw图像配置
rawmode = int(config.get('CAMERA', 'rawmode'))


def customconfig():
    """自定义图像传感器配置，并修改create_still_configuration"""
    # 图像翻转
    hflip = int(config.get('CAMERA', 'hflip'))
    vflip = int(config.get('CAMERA', 'vflip'))
    # display配置
    dphsize = int(config.get('CAMERA', 'dphsize'))
    dpvsize = int(config.get('CAMERA', 'dpvsize'))
    # image配置
    imghsize = int(config.get('CAMERA', 'imghsize'))
    imgvsize = int(config.get('CAMERA', 'imgvsize'))

    # 配置display lores流
    picam2.still_configuration.enable_lores()
    picam2.still_configuration.lores.size = (dphsize, dpvsize)
    # 配置image raw流
    picam2.still_configuration.enable_raw()
    picam2.still_configuration.size = (imghsize, imgvsize)
    # 设置配置文件
    return "still"


# 读取相机配置文件
configname = config.get('CAMERA', 'config')
if configname == 'still':
    camera_config = picam2.create_still_configuration(raw = picam2.sensor_modes[rawmode])
elif configname == 'preview':
    camera_config = picam2.create_preview_configuration()
elif configname == 'video':
    camera_config = picam2.create_video_configuration()
elif configname == 'custom':
    camera_config = customconfig()
else:
    warn("配置文件[CAMERA] 'config' 不符合要求")

previewconfig = picam2.create_preview_configuration()

#拍摄控制参数
shutter = int(config.get('CAMERA', 'shutter'))
gain = float(config.get('CAMERA', 'gain'))


def camera_init():
    """摄像头启动初始化,加载配置文件"""
    picam2.configure(camera_config)
    picam2.controls.ExposureTime = shutter
    picam2.controls.AnalogueGain = gain
    picam2.start()
    print('Raspberry Pi摄像头初始化')
    return 0


def camera_preview(show=True):
    """启用预览

    :param show: 预览形式，默认为True
    """
    picam2.stop_preview()
    picam2.start_preview(show)
    print(show, '预览已切换')
    return 0


shootmode = config.get('CAMERA', 'shootmode')


def shoot(mode=shootmode):
    """拍摄一张图片

    ::param mode: 支持    矩阵-array 和   PIL图像-image
    ::return: 矩阵(array)或PIL库图像(image)
    """
    if mode == 'array':
        return picam2.capture_array("raw")
    elif mode == 'image':
        return picam2.capture_image("raw")


# def reboot():

if not __name__ == '__main__':
    camera_init()

print('图像传感器模块初始化完成')
