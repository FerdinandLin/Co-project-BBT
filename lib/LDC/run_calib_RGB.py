# -*- coding: utf-8 -*-
"""
Calibrate the Camera with Zhang Zhengyou Method.
Picture File Folder: "./pic/RGB_camera_calib_img/", Without Distortion. 

By You Zhiyuan, 2022.07.04, zhiyuanyou@foxmail.com
"""

import os

from calibrate_helper import Calibrator

import configparser

config = configparser.ConfigParser()
if __name__ == '__main__':
    confpath = '../../conf/config.ini'
else:
    confpath = './conf/config.ini'
config.read(confpath, encoding='utf-8')


def main():
    if __name__ == '__main__':
        img_dir = "./pic/RGB_camera_calib_img"
    else:
        img_dir = "./lib/LDC/pic/RGB_camera_calib_img"
    shape_inner_corner = (int(config.get('LDC', 'innercorner1')), int(config.get('LDC', 'innercorner2')))
    size_grid = float(config.get('LDC', 'innercorner1'))
    # create calibrator
    calibrator = Calibrator(img_dir, shape_inner_corner, size_grid)
    # calibrate the camera
    mat_intri, coff_dis = calibrator.calibrate_camera()


if __name__ == '__main__':
    main()
