import playsound
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox,QDialog
from PyQt5.QtCore import Qt
import sys


class ResultUi(QDialog):

    def __init__(self,number,time):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("result.ui", self)
        self.number = number
        self.time = time
        
