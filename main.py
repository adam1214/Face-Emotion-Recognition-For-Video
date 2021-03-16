#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on TUE July 21 10:00:00 2020

@author: Chun-Yu Chen

"""
import sys
import time
import video_emotion_color_demo

if __name__ == "__main__":
    cur_time_zip_name = str(time.ctime()) + '.zip'
    # argc
    argc = len(sys.argv)
    if argc == 7:
        video_emotion_color_demo.fun(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]),  str(sys.argv[6]))
    elif argc == 6:
        video_emotion_color_demo.fun(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]),  cur_time_zip_name)

    print('input file path:', str(sys.argv[1]))
    print('output video & info file path:', str(sys.argv[2]))
    print('input finished path:', str(sys.argv[3]))
    print('model path:', str(sys.argv[4]))
    print('Input video would be resized to '+str(sys.argv[5])+' to process. If input video resolution is less than 720p, it would be processed according to its original resolution.' )
    if argc == 7:
        print('Compressed file name:', str(sys.argv[6]))
    elif argc == 6:
        print('Compressed file name:', cur_time_zip_name)

