#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = 'Webカメラから画像を取得する'
#

import cv2
import time
import argparse
import numpy as np

import Tools.imgfunc as I
import Tools.func as F


def command():
    parser = argparse.ArgumentParser(description=help)
    parser.add_argument('--channel', '-c', type=int, default=0,
                        help='使用するWebカメラのチャンネル [default: 0]')
    parser.add_argument('-o', '--out_path', default='./capture/',
                        help='画像の保存先 (default: ./capture/)')
    parser.add_argument('--img_rate', '-r', type=float, default=1,
                        help='表示する画像サイズの倍率 [default: 1]')
    parser.add_argument('--lower', action='store_true',
                        help='select timeoutが発生する場合に画質を落とす')
    parser.add_argument('--viewer', action='store_true',
                        help='imshowを使用するモード')
    parser.add_argument('--debug', action='store_true',
                        help='debugモード')
    return parser.parse_args()


class videoCap(object):

    def __init__(self, h, w, ch=1, cap_num=6, interval=0.5):
        self.cap = [I.blank.white(h, w, ch) for i in range(cap_num)]
        self.ch = ch
        self.interval = interval
        self.st = time.time()
        self.num = 0

    def check(self):
        tm = time.time() - self.st
        if tm > self.interval:
            return True
        else:
            return False

    def update(self, img):
        if self.ch == 1:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        self.cap.pop(0)
        self.cap.append(img)
        self.st = time.time()

    def viewAll(self, resize=0.5):
        return I.cnv.resize(np.hstack(self.cap), resize)

    def view4(self, resize=0.5):
        return I.cnv.resize(I.cnv.vhstack(self.cap[0:4], (2, 2)), resize)

    def write4(self, out_path, resize=0.5):
        return I.io.write(out_path, 'cap-', self.view4(resize))


def main(args):
    cap = cv2.VideoCapture(args.channel)

    if args.lower:
        cap.set(3, 200)
        cap.set(4, 200)
        cap.set(5, 5)
        h, w = (144, 176)
    else:
        h, w = (640, 480)

    video = videoCap(h, w, 1, 6)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            time.sleep(2)

        if args.viewer:
            cv2.imshow('frame', I.cnv.resize(frame, args.img_rate))

        if video.check():
            video.update(frame)

        key = cv2.waitKey(20) & 0xff

        if args.debug:
            print(key)
            cv2.imshow('all', video.viewAll(0.5))
            cv2.waitKey(20)

        # Display the resulting frame
        if key == 27:  # Esc Key
            print('exit!')
            break
        elif key == 13:  # Enter Key
            video.write4(args.out_path)
            if args.viewer:
                cv2.imshow('cap', video.view4(0.5))
                cv2.waitKey(20)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    args = command()
    F.argsPrint(args)

    print('Key bindings')
    print('[Esc] Exit')
    print('[Ent] Capture')

    main(args)
