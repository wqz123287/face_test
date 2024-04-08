from PyQt5 import uic
import sys
import cv2 as cv
from PyQt5.QtWidgets import QApplication, QWidget,QLabel,QMessageBox,QDialog
import PyQt5.QtWidgets as QtWidgets
import multiprocessing
from playsound import playsound
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui

class Dialog(QDialog):
    def __init__(self,command):
        super().__init__()
        uic.loadUi("dialog.ui",self)

        self.set_ui()
        self.slot_init()
        self.command = command


    def set_ui(self):
        self.setModal(True)
        self.lineEdit.setPlaceholderText("请输入停止命令")


    def slot_init(self):
        self.comfirm.clicked.connect(self.judge)


    def judge(self):
        if self.lineEdit.text() == self.command:
            self.accept()


app = QApplication(sys.argv)
dialog = Dialog("string")
dialog.show()
sys.exit(app.exec_())