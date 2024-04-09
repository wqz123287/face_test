from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
import PyQt5.QtWidgets as QtWidgets
import get_ear
from playsound import playsound
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import warn
from scipy.spatial import distance as dist  # 计算空间距离
from imutils import face_utils
from PyQt5.QtGui import QPixmap, QImage
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
        while True:
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


class firstUi(QWidget):

    def __init__(self, DailogUi):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("first.ui", self)

        self.DailogUi = DailogUi
        self.set_ui()
        self.slot_init()
        self.EAR = 0
        self.ALARM_ON = False
        self.EYE_AR_CONSE_FRAMES = 48
        self.COUNTER = 0
        self.work = showLabels(self)
        self.state = False
        self.alarPath = ""

    def set_ui(self):
        self.picture.setPixmap(QPixmap('vO9e6yZC89.jpg'))
        self.picture.setScaledContents(True)
        self.video.setScaledContents(True)

    def slot_init(self):
        self.file.clicked.connect(self.msgPicture)
        self.alarm01.toggled.connect(lambda :self.radio(self.alarm01))
        self.alarm02.toggled.connect(lambda: self.radio(self.alarm02))
        self.alarm03.toggled.connect(lambda: self.radio(self.alarm03))
        self.play_sound.clicked.connect(self._playSound)
        self.comfirm.clicked.connect(self.judge)
        self.lineEdit.editingFinished.connect(lambda: dialog.getCommand(self.lineEdit.text()))

    def msgPicture(self, Filepath):
        # 点击按钮出现文件夹位置
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选择上传的人脸", "./",
                                                                   "Images (*.png *.xpm *.jpg)")  # 起始路径
        self.path.setText(fileName)
        self.showPicture(fileName)
        self.EAR = get_ear.get_ear(fileName)


    def radio(self,button):
        if button.text() ==  "音频1":
            if button.isChecked():
                self.alarPath = "./audio/alarm.wav"

    def showPicture(self, FilePath):
        if FilePath != '':
            pixmap = QPixmap(FilePath)
            self.picture.setPixmap(pixmap)

    def judge(self):
        if self.path.text() == '':
            self.showMessage("请选择图片")
        elif self.EAR == 0:
            self.showMessage("请重新提供合适的照片")
        elif self.alarmPath.text() == '':
            self.showMessage('请选择音频')
        elif self.lineEdit.text() == '':
            self.showMessage('请输入停止字符')
        else:
            self.show_camera()

    def _playSound(self):

        if self.alarmPath.text() == '':
            self.showMessage('请选择音频')
        else:
            playsound((self.alarmPath.text()))

    def showMessage(self, messsage):
        QMessageBox.warning(self, "警告", messsage, QMessageBox.Cancel)

    def show_camera(self):
        self.work.start()
        self.work.trigger.connect(self.showWarn)

    def showWarn(self):
        if self.state == False:
            self.state = True
            warn.warning(self.lineEdit.text(), self.alarmPath.text())
            self.state = False
        else:
            pass


class DailogUi(QDialog):

    def __init__(self):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("dialog.ui", self)
        self.command = ""

        self.set_ui()
        self.slot_init()

    def getCommand(self, _string):
        self.command = _string

    def set_ui(self):
        self.setModal(True)
        self.lineEdit.setPlaceholderText("请输入停止命令")

    def slot_init(self):
        self.comfirm.clicked.connect(self.judge)

    def judge(self):
        if self.lineEdit.text() == self.command:
            self.accept()


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    dialog = DailogUi()
    firstUi = firstUi(dialog)
    firstUi.show()
    sys.exit(app.exec_())
