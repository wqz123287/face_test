from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
import PyQt5.QtWidgets as QtWidgets
import get_ear
from playsound import playsound
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import warn
from imutils import face_utils
from PyQt5.QtGui import QPixmap, QImage
import playsound
import dlib
import cv2
import time
import imutils
from show_labels import showLabels

def sound_alarm(path):  # 播放提示铃声
    playsound.playsound(path)






class firstUi(QWidget):

    def __init__(self, DailogUi):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("first.ui", self)

        self.DailogUi = DailogUi
        self.set_ui()
        self.slot_init()
        self.EAR = int(0)
        self.ALARM_ON = False
        self.EYE_AR_CONSE_FRAMES = 20
        self.COUNTER = 0
        self.work = showLabels(self)
        self.state = False
        self.alarmPath = "./audio/alarm.wav"
        self.running = True

    def set_ui(self):
        self.picture.setPixmap(QPixmap('vO9e6yZC89.jpg'))
        self.picture.setScaledContents(True)
        self.video.setScaledContents(True)
        self.alarm01.setChecked(True)
        self.over.setEnabled(False)

    def slot_init(self):
        self.play_sound.clicked.connect(self._playSound)
        self.file.clicked.connect(self.msgPicture)
        self.alarm01.toggled.connect(lambda :self.radio(self.alarm01))
        self.alarm02.toggled.connect(lambda: self.radio(self.alarm02))
        self.alarm03.toggled.connect(lambda: self.radio(self.alarm03))
        self.play_sound.clicked.connect(self._playSound)
        self.comfirm.clicked.connect(self.judge)
        self.lineEdit.editingFinished.connect(lambda: dialog.getCommand(self.lineEdit.text()))
        self.over.clicked.connect(self.overProgram)

    def msgPicture(self, Filepath):
        # 点击按钮出现文件夹位置
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(None, "选择上传的人脸", "./",
                                                                   "Images (*.png *.xpm *.jpg)")  # 起始路径

        self.EAR = get_ear.get_ear(fileName)
        if self.EAR == None:
            self.showMessage("未识别到人脸，请更换上传图片")
        else:
            self.showPicture(fileName)
            self.path.setText(fileName)




    def radio(self,button):
        if button.text() ==  "音频1":
            if button.isChecked():
                self.alarmPath = "./audio/alarm.wav"
        elif button.text() ==  "音频2":
            if button.isChecked():
                self.alarmPath = "./audio/alarm_02.mp3"
        elif button.text() == "音频3":
            if button.isChecked():
                self.alarmPath = "./audio/alarm_03.mp3"

    def showPicture(self, FilePath):
        if FilePath != '':
            pixmap = QPixmap(FilePath)
            self.picture.setPixmap(pixmap)

    def judge(self):
        if self.path.text() == '':
            self.showMessage("请选择图片")
        elif self.lineEdit.text() == '':
            self.showMessage('请输入停止字符')
        else:
            self.over.setEnabled(True)
            self.file.setEnabled(False)
            self.play_sound.setEnabled(False)
            self.lineEdit.setEnabled(False)
            self.comfirm.setEnabled(False)
            self.alarm01.setEnabled(False)
            self.alarm02.setEnabled(False)
            self.alarm03.setEnabled(False)

            self.show_camera()

    def _playSound(self):
        for i in range(2):
            playsound.playsound(self.alarmPath)

    def showMessage(self, messsage):
        QMessageBox.warning(self, "警告", messsage, QMessageBox.Cancel)

    def show_camera(self):
        self.work.start()
        self.work.trigger.connect(self.showWarn)

    def showWarn(self):
        if self.state == False:
            self.state = True
            warn.warning(self.lineEdit.text(), self.alarmPath)
            self.state = False
        else:
            pass


    def overProgram(self):
        self.running = False
        self.over.setEnabled(False)
        self.file.setEnabled(True)
        self.play_sound.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.comfirm.setEnabled(True)
        self.alarm01.setEnabled(True)
        self.alarm02.setEnabled(True)
        self.alarm03.setEnabled(True)
        self.picture.setPixmap(QPixmap('vO9e6yZC89.jpg'))
        time.sleep(1.0)
        self.running = True


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
