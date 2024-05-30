from PyQt5.QtCore import QTimer,QThread,pyqtSignal


class myThread(QThread):
    mySignal = pyqtSignal(str)

    def __init__(self, sumTime):
        super(myThread, self).__init__()
        self.sumtime = sumTime

    def __del__(self):
        self.wait()


    def run(self):
        hour = self.sumtime // (3600)
        minute = (self.sumtime - hour * (3600)) // (60)
        second = self.sumtime - hour * 3600 - minute * 60
        if hour < 10:
            hour_str = '0' + str(hour)
        else:
            hour_str = str(hour)
        if minute < 10:
            minute_str = '0' + str(minute)
        else:
            minute_str = str(minute)
        if second < 10:
            second_str = '0' + str(second)
        else:
            second_str = str(second)
        intervals = hour_str + ':' + minute_str + ':' + second_str
        self.mySignal.emit(intervals)


