#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on TUE July 21 10:00:00 2020

@author: Chun-Yu Chen

"""
import sys
import video_emotion_color_demo

if __name__ == "__main__":
    video_emotion_color_demo.fun(
        str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]), str(sys.argv[5]), str(sys.argv[6]))
    print('input file path:', str(sys.argv[1]))
    print('output video file path:', str(sys.argv[2]))
    print('output info file path:', str(sys.argv[3]))
    print('input finished path:', str(sys.argv[4]))
    print('model path:', str(sys.argv[5]))
    print('only process the video that its resolution is '+str(sys.argv[6])+' and above' )
