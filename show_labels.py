from PyQt5.QtCore import QThread, pyqtSignal
from imutils import face_utils
from PyQt5.QtGui import QPixmap, QImage
import dlib
import cv2
import time
import imutils
from scipy.spatial import distance as dist  # 计算空间距离

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear



class showLabels(QThread):
    trigger = pyqtSignal()

    def __init__(self, ui):
        super(showLabels, self).__init__()
        self.ui = ui

    def run(self):
        # show_label._show(self.ui, self.ui.alarmPath.text(), self.ui.video)
        detector = dlib.get_frontal_face_detector()  # 创建人脸检测器
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS[
            'left_eye']  # face_utils.FACIAL_LANDMARKS_IDXS是一个字典，其中包含了人脸的各个部分（如眼睛、鼻子、嘴巴等）对应的特征点的索引
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

        print('[INFO]starting video stream...')

        vs = cv2.VideoCapture(0)
        time.sleep(1.0)
        while self.ui.running:
            hx, frame = vs.read()
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



                if ear < self.ui.EAR:
                    self.ui.COUNTER += 1

                    if self.ui.COUNTER >= self.ui.EYE_AR_CONSE_FRAMES:
                        cv2.putText(frame, 'ALARM', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        if not self.ui.ALARM_ON:
                            self.ui.ALARM_ON = True

                            self.trigger.emit()


                else:
                    self.ui.COUNTER = 0
                    self.ui.ALARM_ON = False
                cv2.putText(frame, 'ERA:{:.2f}'.format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
                            2)

            if self.ui.open_close.currentIndex() == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                Qframe = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(Qframe)
                self.ui.video.setPixmap(pixmap)
            else:
                pixmap = QPixmap("first.png")
                self.ui.video.setPixmap(pixmap)