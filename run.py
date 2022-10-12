# -*- coding:utf-8 -*-
# @FileName    :run.py
# @IDE         :PyCharm
# @Time        :2022/9/1 16:56
# @Author      :Lin
# @Desc        :


from time import sleep
from core import MotorControl
from core import camera
import core.shoot as shoot

print('程序将在3秒后进行初始化...', end='')
sleep(1), print('\r程序将在2秒后进行初始化...', end='')
sleep(1), print('\r程序将在1秒后进行初始化...')
sleep(1), print('\r程序初始化...')


