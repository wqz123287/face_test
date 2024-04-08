import playsound
from threading import Thread
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox,QDialog
from PyQt5.QtCore import Qt
import sys

class Sound:
    def __init__(self,filename):
        self.filename = filename
        self.state = 1
        t = Thread(target=self.playsound)
        t.start()

    def playsound(self):
        while self.state:
            playsound.playsound(self.filename)


class DailogUi(QDialog):

    def __init__(self,command,filename):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("dialog.ui", self)
        self.filename = filename
        self.sound = Sound(self.filename)
        self.command = command
        self.state = 1
        self.set_ui()
        self.slot_init()
        print(command,filename)


    def getCommand(self, _string):
        self.command = _string

    def set_ui(self):
        self.setModal(True)
        self.lineEdit.setPlaceholderText("请输入停止命令")

    def slot_init(self):
        self.comfirm.clicked.connect(self.judge)

    def judge(self):

        if self.lineEdit.text() == self.command:
            self.sound.state =0
            self.accept()
            pass








def warning(command,filename):

    dialog = DailogUi(command,filename)
    dialog.show()
    dialog.exec_()



