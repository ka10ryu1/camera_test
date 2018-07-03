#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = 'Webカメラから画像を取得する'
#

import logging
# basicConfig()は、 debug()やinfo()を最初に呼び出す"前"に呼び出すこと
level = logging.INFO
logging.basicConfig(format='%(message)s')
logging.getLogger('Tools').setLevel(level=level)

import cv2
import time
import argparse

import Tools.func as F
from Lib.video import videoCap


def command():
    parser = argparse.ArgumentParser(description=help)
    parser.add_argument('-c', '--channel', type=int, default=0,
                        help='使用するWebカメラのチャンネル [default: 0]')
    parser.add_argument('-o', '--out_path', default='./capture/',
                        help='画像の保存先 (default: ./capture/)')
    parser.add_argument('-i', '--interval_time', type=float, default=0.5,
                        help='インターバル撮影の間隔 [default: 0.5]')
    parser.add_argument('-s', '--stock_num', type=int, default=6,
                        help='インターバル撮影の画像保持数 [default: 6]')
    parser.add_argument('--lower', action='store_true',
                        help='select timeoutが発生する場合に画質を落とす')
    parser.add_argument('--debug', action='store_true',
                        help='debugモード')
    args = parser.parse_args()
    F.argsPrint(args)
    return args


def main(args):
    cap = videoCap(args.channel, 1, args.lower,
                   args.stock_num, args.interval_time)
    while(True):
        # カメラ画像の取得
        if cap.read() is False:
            print('camera read false ...')
            time.sleep(2)
            continue

        # 画面の表示とキー入力の取得
        cv2.imshow('all', cap.viewAll())
        key = cv2.waitKey(20) & 0xff
        if args.debug:
            print('key: {}, frame: {}'.format(key, cap.frame_shape))

        # キーに応じて制御
        if key == 27:  # Esc Key
            print('exit!')
            break
        elif key == 13 or key == 10:  # Enter Key
            print('capture:', cap.write4(args.out_path))
            if args.debug:
                cv2.imshow('cap', cap.view4())

    # 終了処理
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    print('Key bindings')
    print('[Esc] Exit')
    print('[Ent] Capture')
    main(command())
