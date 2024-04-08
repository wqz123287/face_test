from scipy.spatial import distance as dist # 计算空间距离
from imutils import face_utils
from threading import Thread    # 多线程
from PyQt5.QtGui import QPixmap,QImage
import playsound
import dlib
import cv2
import time
import imutils
import warn

def sound_alarm(path):  # 播放提示铃声
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear

def _show(self,filename,label):
    detector = dlib.get_frontal_face_detector()  # 创建人脸检测器
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS[
        'left_eye']  # face_utils.FACIAL_LANDMARKS_IDXS是一个字典，其中包含了人脸的各个部分（如眼睛、鼻子、嘴巴等）对应的特征点的索引
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

    print('[INFO]starting video stream...')

    vs = cv2.VideoCapture(0)
    time.sleep(1.0)
    while True:
        hx,frame = vs.read()
        frame = imutils.resize(frame, width=450)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 0)

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < self.EAR:
                cv2.putText(frame, 'ALARM', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                if not self.ALARM_ON:
                    self.ALARM_ON = True

                    return "warning"


            else:
                self.COUNTER = 0
                self.ALARM_ON = False
            cv2.putText(frame, 'ERA:{:.2f}'.format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        if self.open_close.currentIndex() == 0:
            print("show")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            Qframe = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(Qframe)
            self.video.setPixmap(pixmap)
        else :
            pixmap = QPixmap("first.png")
            self.video.setPixmap(pixmap)


