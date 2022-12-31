# -*- coding: utf-8 -*-
# @Time : 2021/9/11 18:48
# @Author : 67689e4f
# @Email : 964342226@qq.com
# @File : camera.py

import ctypes
import time
from multiprocessing import Process, Value, sharedctypes

import cv2
import numpy as np
from camera import Camera_p

WIDTH = 1920
HEIGHT = 1080

class Camera_p(Process):
    def __init__(self, arr, isGrab):
        super(Camera_p, self).__init__()
        self.arr = arr
        self.isGrab = isGrab

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.isGrab.value:
            _, frame = cap.read()
            cv2.waitKey(1)
            frame = frame.flatten(order='C')
            t_0 = time.time()
            temp = np.frombuffer(self.arr, dtype=np.uint8)
            temp[:] = frame
            # self.arr[:] = frame #需要0.1秒
            t_1 = time.time()
            print(t_1 - t_0)


class Show_window():
    def __init__(self):
        self.camera_arr = sharedctypes.RawArray(ctypes.c_int8, WIDTH * HEIGHT * 3)
        self.isGrab = Value('i', True)

    def showpic(self):
        cam_pro = Camera_p(self.camera_arr, self.isGrab)
        cam_pro.start()

        while True:
            frame_show = np.frombuffer(self.camera_arr, dtype=np.uint8).reshape(WIDTH, HEIGHT, 3)
            cv2.imshow('0', frame_show)
            key = cv2.waitKey(50)
            if key == ord('q'):
                self.isGrab.value = False
                break


def main():
    show = Show_window()
    show.showpic()


if __name__ == '__main__':
    main()
