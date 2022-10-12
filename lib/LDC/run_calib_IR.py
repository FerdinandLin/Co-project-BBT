# -*- coding: utf-8 -*-
"""
Calibrate the Camera with Zhang Zhengyou Method.
Picture File Folder: "./pic/IR_camera_calib_img/", With Distortion. 

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
        save_dir = "./pic/IR_dedistortion"
    else:
        img_dir = "./lib/LDC/pic/RGB_camera_calib_img"
        save_dir = "./lib/LDC/pic/IR_dedistortion"
    shape_inner_corner = (int(config.get('LDC', 'innercorner1')), int(config.get('LDC', 'innercorner2')))
    size_grid = float(config.get('LDC', 'innercorner1'))
    # create calibrator
    calibrator = Calibrator(img_dir, shape_inner_corner, size_grid)
    # calibrate the camera
    mat_intri, coff_dis = calibrator.calibrate_camera()
    # dedistort and save the dedistortion result
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    calibrator.dedistortion(save_dir)


if __name__ == '__main__':
    main()
