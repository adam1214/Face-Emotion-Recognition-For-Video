#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 17:33:00 2020

@author: peterwu and Chun-Yu Chen

"""
# import sys
from statistics import mode
import time

import glob
import csv
import codecs
import shutil
import os
import stat
import cv2
import numpy as np
import zipfile

from os.path import join
from keras.models import load_model
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

#Detecting face emotion on input video

def fun(in_path, out_info_path, in_finished_path, model_path, video_resolution, zip_name):
    """
     >>>  fun(/fer_input, /fer_result, /fer_finished, /fer_model, video_resolution, zip_name)
    .mp4 files in the fer_intput folder will move to fer_finished folder.
    Processed .mp4 files will be saved in fer_output folder.
    .csv files will be saved in fer_result folder.
    Input video would be resized to 720p to process.  If input video resolution is less than 720p, it would be processed according to its original resolution.
    """
    detect_emo = True

    #save config
    save_video = True
    save_info = True

    show_video = False

    #config = tf.ConfigProto()
    # config.gpu_options.per_process_gpu_memory_fraction = 0.7
    # config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)
    #%%
    # parameters for loading data and images
    detection_model_path = model_path +  '/haarcascade_frontalface_default.xml'
    if detect_emo:
        emotion_model_path = model_path + '/fer2013_mini_XCEPTION.102-0.66.hdf5'
        emotion_labels = get_labels('fer2013')
        emotion_offsets = (20, 40)
        # loading models
        emotion_classifier = load_model(emotion_model_path, compile=False)
        # getting input model shapes for inference
        emotion_target_size = emotion_classifier.input_shape[1:3]
        # starting lists for calculating modes
        emotion_window = []

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # loading models
    face_detection = load_detection_model(detection_model_path)

    info_name = ['time', 'frame', 'face_idx', 'face_x', 'face_y', 'face_w', 'face_h', 'emotion']

    input_video_root = in_path
    output_info_root = out_info_path
    for video_path in glob.glob(input_video_root+'/**/*.mp4', recursive=True):
        print(video_path)
        no_root_path = video_path[len(input_video_root):].replace(video_path.split('/')[-1], '')
        video_capture = cv2.VideoCapture(video_path)
        video_cap_ori = cv2.VideoCapture(video_path)
        video_name = video_path.split('/')[-1].split('.mp4')[0]
        ori_video_name = video_path.split('/')[-1]

        fps_float = video_capture.get(cv2.CAP_PROP_FPS)
        fps = round(video_capture.get(cv2.CAP_PROP_FPS))
        size = (round(video_capture.get(3)), round(video_capture.get(4))) # float
        ori_size = size
        reduce_resolution = 0
        scaling_factor_x = 1
        scaling_factor_y = 1

        if video_resolution == "720p" and (size[0] > 1280 or size[1] > 720):
            #need to reduce resolution to 720p
            reduce_resolution = 1
            out_path = input_video_root + no_root_path+'resize_to_720p_'+video_path.split('/')[-1]
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            out = cv2.VideoWriter(out_path,fourcc, fps, (1280,720))
            while True:
                ret, frame = video_capture.read()
                if ret == True:
                    b = cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                    out.write(b)
                else:
                    break
            video_capture.release()
            out.release()
            
            scaling_factor_x = size[0]/1280
            scaling_factor_y = size[1]/720

            #original resolution video move to fer_finished dir 
            src = video_path
            dst = in_finished_path + no_root_path + video_name + ".mp4"
            os.makedirs(os.path.dirname(in_finished_path + no_root_path), exist_ok=True)
            shutil.move(src, dst)

            #capture ori resolution video to draw bounding box
            video_cap_ori = cv2.VideoCapture(dst)

            #capture reducing resolution video to construct csv file
            video_path = out_path
            video_capture = cv2.VideoCapture(video_path)
            video_name = video_path.split('/')[-1].split('.mp4')[0]
            fps_float = video_capture.get(cv2.CAP_PROP_FPS)
            fps = round(video_capture.get(cv2.CAP_PROP_FPS))
            size = (round(video_capture.get(3)), round(video_capture.get(4))) # float

        if True:
            if save_video:
                os.makedirs(os.path.dirname(output_info_root + no_root_path), exist_ok=True)
                out_path = output_info_root+no_root_path+ori_video_name
                fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                out = cv2.VideoWriter(out_path, fourcc, fps, ori_size)
            if save_info:
                os.makedirs(os.path.dirname(output_info_root + no_root_path), exist_ok=True)
                csv_info = codecs.open(
                    output_info_root+no_root_path+video_name+'_info.csv', 'w', encoding="utf_8_sig"
                )
                csv_writer = csv.writer(csv_info)
                csv_writer.writerow(info_name)

            frame_idx = 0
            st_time = time.time()
            while (video_cap_ori.isOpened()):
                if frame_idx % 10 == 0:
                    print('Processing frame: '+ str(frame_idx)+' ......')

                video_flag_ori, bgr_image_ori = video_cap_ori.read() #ori image
                video_flag, bgr_image = video_capture.read() #downscale image

                if video_flag:
                    frame_idx += 1
                    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
                    #rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

                    #gray_image_ori = cv2.cvtColor(bgr_image_ori, cv2.COLOR_BGR2GRAY)
                    #rgb_image_ori = cv2.cvtColor(bgr_image_ori, cv2.COLOR_BGR2RGB)

                    faces = detect_faces(face_detection, gray_image)
                    if not isinstance(faces, tuple):
                        faces = faces[faces[:,0].argsort()]
                    
                    face_idx = 1
                    for face_coordinates in faces:
                        x_1, x_2, y_1, y_2 = apply_offsets(face_coordinates, emotion_offsets)

                        if detect_emo:
                            gray_face = gray_image[y_1:y_2, x_1:x_2]
                            try:
                                gray_face = cv2.resize(gray_face, (emotion_target_size))
                            except:
                                continue

                            gray_face = preprocess_input(gray_face, True)
                            gray_face = np.expand_dims(gray_face, 0)
                            gray_face = np.expand_dims(gray_face, -1)

                            emotion_prediction = emotion_classifier.predict(gray_face)
                            emotion_probability = np.max(emotion_prediction)
                            emotion_label_arg = np.argmax(emotion_prediction)
                            emotion_text = emotion_labels[emotion_label_arg]
                            emotion_window.append(emotion_text)

                            if len(emotion_window) > frame_window:
                                emotion_window.pop(0)
                            try:
                                emotion_mode = mode(emotion_window)
                            except:
                                continue
                            x = int(float(face_coordinates[0]*scaling_factor_x))
                            y = int(float(face_coordinates[1]*scaling_factor_y))
                            w = int(float(face_coordinates[2]*scaling_factor_x))
                            h = int(float(face_coordinates[3]*scaling_factor_y))
                            if emotion_text == 'angry':
                                # setup text
                                font = cv2.FONT_HERSHEY_TRIPLEX
                                text = str(face_idx).zfill(2)+'-angry'

                                # get boundary of this text
                                textsize = cv2.getTextSize(text, font, 1, 2)[0]

                                # get coords based on boundary
                                textX = (w - textsize[0]) / 2 + x
                                textY = y - 12

                                cv2.rectangle(bgr_image_ori, (x, y), (x+w, y+h), (255,0,0), 4)
                                cv2.putText(bgr_image_ori, text, (int(textX), int(textY)), font, 1.5, (255, 0, 0), 1, cv2.LINE_AA)
                            elif emotion_text == 'sad':
                                # setup text
                                font = cv2.FONT_HERSHEY_TRIPLEX
                                text = str(face_idx).zfill(2)+'-sad'

                                # get boundary of this text
                                textsize = cv2.getTextSize(text, font, 1, 2)[0]

                                # get coords based on boundary
                                textX = (w - textsize[0]) / 2 + x
                                textY = y - 12

                                cv2.rectangle(bgr_image_ori, (x, y), (x+w, y+h), (0,0,255), 4)
                                cv2.putText(bgr_image_ori, text, (int(textX), int(textY)), font, 1.5, (0,0,255), 1, cv2.LINE_AA)
                            elif emotion_text == 'happy':
                                # setup text
                                font = cv2.FONT_HERSHEY_TRIPLEX
                                text = str(face_idx).zfill(2)+'-happy'

                                # get boundary of this text
                                textsize = cv2.getTextSize(text, font, 1, 2)[0]

                                # get coords based on boundary
                                textX = (w - textsize[0]) / 2 + x
                                textY = y - 12

                                cv2.rectangle(bgr_image_ori, (x, y), (x+w, y+h), (255,255,0), 4)
                                cv2.putText(bgr_image_ori, text, (int(textX), int(textY)), font, 1.5, (255,255,0), 1, cv2.LINE_AA)
                            elif emotion_text == 'surprise':
                                # setup text
                                font = cv2.FONT_HERSHEY_TRIPLEX
                                text = str(face_idx).zfill(2)+'-surprise'

                                # get boundary of this text
                                textsize = cv2.getTextSize(text, font, 1, 2)[0]

                                # get coords based on boundary
                                textX = (w - textsize[0]) / 2 + x
                                textY = y - 12

                                cv2.rectangle(bgr_image_ori, (x, y), (x+w, y+h), (0,255,255), 4)
                                cv2.putText(bgr_image_ori, text, (int(textX), int(textY)), font, 1.5, (0,255,255), 1, cv2.LINE_AA)
                            else:
                                # setup text
                                font = cv2.FONT_HERSHEY_TRIPLEX
                                text = str(face_idx).zfill(2)+'-neutral'

                                # get boundary of this text
                                textsize = cv2.getTextSize(text, font, 1, 2)[0]

                                # get coords based on boundary
                                textX = (w - textsize[0]) / 2 + x
                                textY = y - 12

                                cv2.rectangle(bgr_image_ori, (x, y), (x+w, y+h), (0,255,0), 4)
                                cv2.putText(bgr_image_ori, text, (int(textX), int(textY)), font, 1.5, (0,255,0), 1, cv2.LINE_AA)
                            
                        if not detect_emo:
                            color = np.asarray((0, 0, 0))
                            color = color.astype(int)
                            color = color.tolist()
                            draw_bounding_box(face_coordinates, rgb_image, color)

                        if save_info:
                            op_info_list = [round(frame_idx/fps_float, 3), frame_idx, str(face_idx).zfill(2),
                                            face_coordinates[0]*scaling_factor_x, face_coordinates[1]*scaling_factor_y,
                                            face_coordinates[2]*scaling_factor_x, face_coordinates[3]*scaling_factor_y]
                            for i in range(len(op_info_list)):
                                op_info_list[i] = str(op_info_list[i])
                            if detect_emo:
                                op_info_list.append(emotion_text)
                            csv_writer.writerow(op_info_list)
                        face_idx += 1

                    #bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

                    if save_video:
                        out.write(bgr_image_ori)
                    if show_video:
                        cv2.imshow('window_frame', bgr_image)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                else:
                    break
            if save_video:
                out.release()
            if save_info:
                csv_info.close()
            print(video_path+' DONE!!\tSpend Time: '+str(time.time()-st_time)+'(s)')
            video_capture.release()
            video_cap_ori.release()
            if show_video:
                cv2.destroyAllWindows()

        else:
            os.makedirs(os.path.dirname(output_info_root + no_root_path), exist_ok=True)
            csv_info = codecs.open(output_info_root+no_root_path+video_name+'_info.csv',
                                'w', encoding="utf_8_sig")
            csv_writer = csv.writer(csv_info)
            err_msg = "The resolution of " + video_name + ".mp4 is lower than 720p."
            csv_writer.writerow([err_msg])
            csv_info.close()

        src = video_path
        dst = in_finished_path + no_root_path + video_name + ".mp4"
        os.makedirs(os.path.dirname(in_finished_path + no_root_path), exist_ok=True)
        shutil.move(src, dst)
        if reduce_resolution == 1:
            video_ori_name = video_name[15:]
            csv_path_rename = output_info_root+no_root_path+video_name+'_info.csv'
            os.remove(dst)
            os.rename(output_info_root+no_root_path+video_name+'_info.csv', output_info_root+no_root_path+video_ori_name+'_info.csv')

    shutil.rmtree(input_video_root, ignore_errors=True)
    if input_video_root == 'fer_input/':
        os.makedirs('fer_input/', stat.S_IRWXO + stat.S_IRWXG + stat.S_IRWXU)

    with zipfile.ZipFile('fer_result/' + zip_name, 'w') as zf:
        for root, dirs, files in os.walk('fer_result/'):
            for file_name in files:
                if '.zip' not in file_name and '.gitkeep' not in file_name:
                    fullpath = join(root, file_name)
                    #print(fullpath)
                    zf.write(fullpath, fullpath[len('fer_result/'):])
                    os.remove(fullpath)
            if root != 'fer_result/':
                shutil.rmtree(root)