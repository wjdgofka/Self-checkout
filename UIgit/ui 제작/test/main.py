import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

running = False
log = False

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.bill = QTextBrowser(self)
        self.bill.move(880,10)
        self.bill.resize(230,460)
        self.bill.setPlainText('test')

        self.billresult = QLabel(self)
        self.billresult.move(880,480)
        self.billresult.setText('총합')

        self.label1 = QLabel(self)
        self.label1.move(10,10)

        self.starbt = QPushButton('on', self)
        self.starbt.move(10,510)
        self.starbt.resize(80,30)

        self.stopbt = QPushButton('stop', self)
        self.stopbt.move(100,510)
        self.stopbt.resize(80,30)

        self.admin = QPushButton('admin', self)
        self.admin.move(190, 510)
        self.admin.resize(80, 30)

        self.count = QPushButton('계산하기', self)
        self.count.move(880,510)
        self.count.resize(80,30)

        self.login = QPushButton('login', self)
        self.login.move(970,510)
        self.login.resize(80,30)

        self.setWindowTitle('testing')
        self.setGeometry(300, 300, 1120, 550)
        self.show()

        self.app =QApplication([])

        self.login.clicked.connect(self.chout)
        self.starbt.clicked.connect(self.start)
        self.stopbt.clicked.connect(self.stop)
        self.count.clicked.connect(self.countrun)
        self.admin.clicked.connect(self.adminlog)
        self.app.aboutToQuit.connect(self.onExit)

    def countrun(self):
        self.bill.clear()
        th = threading.Thread(target=self.billcount)
        th.start()

    def billcount(self):
        self.bill.append('상품 : cho 가격 : 1500')


    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def run(self):
        global running
        cap = cv2.VideoCapture(0)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.label1.resize(width, height)
        while running:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                p = pixmap.scaled(int(w * 480 / h), 480, QtCore.Qt.IgnoreAspectRatio)
                self.label1.resize((w * 480 / h), 480 )
                self.label1.setPixmap(p)
            else:
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")

    def stop(self):
        global running
        running = False
        print("stoped..")

    def onExit(self):
        print("exit")
        self.stop()

    def chout(self):
        th = threading.Thread(target=self.loginout)
        th.start()

    def loginout(self):
        global log
        if log:
            log = False
            self.login.setText('login')
        else:
            log = True
            self.login.setText('logout')

    def adminlog(self):
        th = threading.Thread(target=self.adminlogin)
        th.start()

    def adminlogin(self):
        print('x')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
