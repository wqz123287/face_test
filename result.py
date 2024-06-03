from PyQt5 import uic
from PyQt5.QtWidgets import QDialog



class ResultUi(QDialog):

    def __init__(self,number,time):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("result.ui", self)
        self._number,self._time = self.change(number,time)
        self.number.setText(self._number)
        self.time.setText(self._time)

    def change(self,number,time):
        info = time.split(':')
        for i in range(3):
            info[i] = int(info[i])
        if info[2] == 0:
            info[2]=59
            if info[1]==0:
                info[1]=59
                info[0] = info[0]-1
            else:
                info[1] = info[1] - 1
        else:
            info[2] = info[2]-1
        result_time = '本次一共检测了'+str(info[0])+'小时'+str(info[1])+'分钟'+str(info[2])+'秒'
        result_number = '一共走神了'+str(number)+'次'
        return result_number,result_time

def result(number,time):
    ui = ResultUi(number,time)
    ui.show()
    ui.exec_()