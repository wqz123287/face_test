from scipy.spatial import distance as dist # 计算空间距离
from imutils.video import VideoStream   # 处理视频流
from imutils import face_utils
from threading import Thread    # 多线程
import numpy as np
import playsound

import dlib
import cv2
import time
import imutils


def sound_alarm(path):  # 播放提示铃声
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0],eye[3])

    ear = (A+B)/(2.0*C)
    return ear


def facialLandmarks():
    detector = dlib.get_frontal_face_detector()  # 创建人脸检测器
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS[
        'left_eye']  # face_utils.FACIAL_LANDMARKS_IDXS是一个字典，其中包含了人脸的各个部分（如眼睛、鼻子、嘴巴等）对应的特征点的索引
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
    return detector,predictor,lStart,lEnd,rStart,rEnd

def processing()