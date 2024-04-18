from scipy.spatial import distance as dist # 计算空间距离

from imutils import face_utils

import dlib
import cv2

import imutils


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0],eye[3])

    ear = (A+B)/(2.0*C)
    return ear


def get_ear(filename):
    detector = dlib.get_frontal_face_detector()  # 创建人脸检测器
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS[
        'left_eye']  # face_utils.FACIAL_LANDMARKS_IDXS是一个字典，其中包含了人脸的各个部分（如眼睛、鼻子、嘴巴等）对应的特征点的索引
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

    frame = cv2.imread(filename)
    frame = imutils.resize(frame,width = 450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)   # 得到的是图片中的所有人脸

    for rect in rects:
        shape = predictor(gray,rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) / 2.0
        print(ear)
        return ear



