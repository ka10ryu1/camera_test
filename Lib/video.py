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

    def __init__(self, usb_ch, img_ch=3, lower=False, cap_num=6, interval=0.5):
        self._cap = cv2.VideoCapture(usb_ch)
        if lower:
            self._cap.set(3, 200)
            self._cap.set(4, 200)
            self._cap.set(5, 5)
            self.size = (144, 176, img_ch)
        else:
            self.size = (480, 640, img_ch)

        # 表示・保存用画像の格納先を確保
        self._frame = I.blank.black(self.size[0], self.size[1], self.size[2])
        self._data = [I.blank.black(self.size[0], self.size[1], self.size[2])
                      for i in range(cap_num)]
        # 保存する画像のチャンネル数
        self.ch = self.size[2]
        # キャプチャ画像のサイズ情報
        self.frame_shape = self._frame.shape
        # インターバル撮影する間隔 [s]
        self.interval = interval
        # タイマー起動
        self._start = time.time()
        # 保存用の連番
        self._num = 0

    def read(self):
        """
        USBカメラから画像を取得し、インターバルを確認する
        """

        # USBカメラから画像を取得する
        ret, frame = self._cap.read()
        if ret is False:
            return ret

        # フレーム情報の確保
        self._frame = frame
        self.frame_shape = frame.shape
        # インターバルが経過していれば、フレームを確保する
        if self.intervalCheck():
            self.update()

        return ret

    def frame(self, rate=1):
        """
        現在のフレームの取得
        """

        return I.cnv.resize(self._frame, rate)

    def intervalCheck(self):
        """
        インターバル撮影の確認
        [out] Trueならインターバルの時間経過
        """

        tm = time.time() - self._start
        if tm > self.interval:
            return True
        else:
            return False

    def update(self):
        """
        インターバル画像のアップデート
        """

        if self.ch == 1:
            img = cv2.cvtColor(self._frame, cv2.COLOR_RGB2GRAY)
        else:
            img = self._frame

        self._data.pop(0)
        self._data.append(img)
        self._start = time.time()

    def viewAll(self, resize=0.5):
        """
        インターバル画像をすべて表示
        [in]  表示するリサイズ率
        [out] 現在のフレームと全インターバル画像を連結したもの
        """

        sub_img = I.cnv.resize(I.cnv.vhstack(self._data, (2, 3)), resize)
        sub_img = cv2.cvtColor(sub_img, cv2.COLOR_GRAY2RGB)
        return np.hstack([self._frame, sub_img])

    def view4(self, resize=0.5):
        """
        インターバル画像の後ろから4枚を表示
        [in]  表示するリサイズ率
        [out] 表示するインターバル画像を後ろから4枚連結したもの
        """

        return I.cnv.resize(I.cnv.vhstack(self._data[0:4], (2, 2)), resize)

    def write4(self, out_path, resize=0.5):
        """
        インターバル画像の後ろから4枚を保存
        [in]  out_path: 保存先のフォルダ名
        [in]  resize:   画像のリサイズ率
        [out] 保存するパス
        """

        return I.io.write(out_path, 'cap-', self.view4(resize))

    def release(self):
        """
        終了処理
        """

        self._cap.release()
