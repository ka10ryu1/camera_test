#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = 'Webカメラの画像管理'
#

import cv2
import time
import numpy as np

import Tools.imgfunc as I


class videoCap(object):
    """
    USBカメラの処理をクラス化したもの
    """

    def __init__(self, size, cap_num=6, interval=0.5):

        if len(size) != 3:
            size = (480, 640, 1)

        # 表示・保存用画像の格納先を確保
        self.cap = [I.blank.white(size[0], size[1], size[2])
                    for i in range(cap_num)]
        # 保存する画像のチャンネル数
        self.ch = size[2]
        # インターバル撮影する間隔 [s]
        self.interval = interval
        # タイマー起動
        self.st = time.time()
        # 保存用の連番
        self.num = 0

    def check(self):
        """
        インターバル撮影の確認
        [out] Trueならインターバルの時間経過
        """

        tm = time.time() - self.st
        if tm > self.interval:
            return True
        else:
            return False

    def update(self, img):
        """
        インターバル画像のアップデート
        [in]  インターバル画像
        """

        if self.ch == 1:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        self.cap.pop(0)
        self.cap.append(img)
        self.st = time.time()

    def viewAll(self, resize=0.5):
        """
        インターバル画像をすべて表示
        [in]  表示する拡大率
        [out] 表示するインターバル画像をすべて連結したもの
        """

        return I.cnv.resize(np.hstack(self.cap), resize)

    def view4(self, resize=0.5):
        """
        インターバル画像の後ろから4枚を表示
        [in]  表示する拡大率
        [out] 表示するインターバル画像を後ろから4枚連結したもの
        """

        return I.cnv.resize(I.cnv.vhstack(self.cap[0:4], (2, 2)), resize)

    def write4(self, out_path, resize=0.5):
        """
        インターバル画像の後ろから4枚を保存
        [in]  保存先のフォルダ名
        [out] 保存するパス
        """

        return I.io.write(out_path, 'cap-', self.view4(resize))
