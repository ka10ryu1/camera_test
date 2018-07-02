#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = 'Webカメラから画像を取得する'
#

import cv2
import time
import argparse

import Tools.imgfunc as I
import Tools.func as F
from Lib.video import videoCap


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
    args = parser.parse_args()
    F.argsPrint(args)
    return args


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
            print('key: {}, frame: {}'.format(key, frame.shape))
            cv2.imshow('all', video.viewAll(0.5))
            cv2.waitKey(20)

        # Display the resulting frame
        if key == 27:  # Esc Key
            print('exit!')
            break
        elif key == 13 or key == 10:  # Enter Key
            video.write4(args.out_path)
            if args.viewer:
                cv2.imshow('cap', video.view4(0.5))
                cv2.waitKey(20)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    print('Key bindings')
    print('[Esc] Exit')
    print('[Ent] Capture')
    main(command())
