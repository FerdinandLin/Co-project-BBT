# -*- coding:utf-8 -*-
# @FileName    :MotorControl
# @IDE         :PyCharm
# @Time        :2022/9/1 22:10
# @Author      :Lin
# @Desc        :

from time import sleep as delay

import sys
import pigpio
import configparser

config = configparser.ConfigParser()
if __name__ == '__main__':
    confpath = '../conf/config.ini'
else:
    confpath = './conf/config.ini'

config.read(confpath, encoding='utf-8')

#   读取驱动器电路接法
anode = config.get('HBS57', 'anode')
if anode == 'True':
    anode = True
elif anode == 'False':
    anode = False
else:
    sys.exit("警告：配置文件[HBS57] 'anode' 不符合要求")
#   使能信号共阴时高电平
ena = 1
if anode:
    ena = 0
    print('驱动器为共阳接法')
else:
    print('驱动器为共阴接法')

#   读取通讯引脚信息
dirio = int(config.get('HBS57', 'DIR'))
pulio = int(config.get('HBS57', 'PUL'))

#   读取时序
#   ENA提前DIR时间(us)
t1 = float(config.get('HBS57', 't1'))/10**6
#   DIR提前PUL时间(us)
t2 = float(config.get('HBS57', 't1'))/10**6
#   脉冲高低电平最短时间(us)
t3 = float(config.get('HBS57', 't3'))/10**6

#   授予对Pi的GPIO的访问权
pi = pigpio.pi()
if not pi.connected:
    sys.exit('警告：GPIO连接出错')

dirlevel = ena


def init():
    """电机启动初始化"""
    pi.set_mode(dirio, pigpio.OUTPUT)
    pi.set_mode(pulio, pigpio.OUTPUT)
    delay(t1)
    pi.write(dirio, ena)
    delay(t2)
    pi.write(pulio, ena)
    delay(t3)
    return 0


def dirflip():
    """电机转动方向翻转"""
    global dirlevel, dirio
    if dirlevel:
        dirlevel = 0
    else:
        dirlevel = 1
    pi.write(dirio, dirlevel)
    delay(t2)
    return 0


def pulse(pultime):
    """PUL线发送一次脉冲

    :param pultime: 脉冲一个周期的时间
    """
    global ena, pulio, t3
    if pultime < t3*2:
        pultime = t3*2
    if ena:
        pul1 = 0
        pul2 = 1
    else:
        pul1 = 1
        pul2 = 0
    pi.write(pulio, pul1)
    delay(pultime/2)
    pi.write(pulio, pul2)
    delay(pultime/2)
    return 0


#   导程
screwlead = float(config.get('leadscrew', 'lead'))
#   细分值
microsteps = float(config.get('HBS57', 'microsteps'))
#   每一微步步进位移距离
microdistance = screwlead/microsteps


def zmove(distance, direct, speed=10):
    """对成像平台进行移动

    :param distance: 平台要位移的距离
    :param direct: 平台位移方向
    :param speed: 平台位移速度(默认10)
    :return:未能完成位移的微步数
    """
    global microdistance
    global dirlevel
    steps = int(distance/microdistance)
    steprem = distance % microdistance
    microsteptime = microsteps/speed
    if direct != dirlevel:
        dirflip()
    for i in range(steps):
        pulse(microsteptime)
    return steprem


print('MotorControl.py 电机控制模块初始化完成')
