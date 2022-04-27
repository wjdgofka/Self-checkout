import cv2
import threading
import sys
import subprocess
import uidetect
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

running = False
log = False

cur_list=[] #현재 있는 물건
index=[] # 상품과 가격 추적하기 위해 존재
list=['cho','moch', 'che', 'songi', 'margaret', 'parkkas', 'skittles', 'wafers', 'wangkkumteulyi','Eclipse','Ghana','Miz']
price=[1500,3000,2500,1500,1000,2000,1500,1500,1000,2000,1000,1500]
accurate_item_list=[] #정확도가 0.9가 넘는 아이템 리스트
accurate_item_num=0  #그중 정확도가 0.9가 넘는 아이템의 개수
sec=5

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.bill = QTextBrowser(self)
        self.bill.move(880,10)
        self.bill.resize(230,470)
        self.bill.setFontPointSize(16)
        self.bill.setPlainText('물품 나오는곳')

        self.billresult = QTextBrowser(self)
        self.billresult.move(880,455)
        self.billresult.resize(230,35)
        self.billresult.setFontPointSize(16)
        self.billresult.setText('총합')

        self.label1 = QLabel(self)
        self.label1.move(10,10)

        self.user = QLabel(self)
        self.user.move(500,520)
        self.user.setText('User :                         ')

        self.starbt = QPushButton('on', self)
        self.starbt.move(10,510)
        self.starbt.resize(80,30)

        self.stopbt = QPushButton('stop', self)
        self.stopbt.move(100,510)
        self.stopbt.resize(80,30)

        '''self.admin = QPushButton('admin', self)
        self.admin.move(190, 510)
        self.admin.resize(80, 30)'''

        self.count = QPushButton('계산하기', self)
        self.count.move(880,500)
        self.count.resize(230,40)

        self.login = QPushButton('login', self)
        self.login.move(190,510)
        self.login.resize(80,30)

        self.setWindowTitle('testing')
        self.setGeometry(300, 300, 1120, 550)
        self.show()

        self.loginwindow = QDialog()

        labelid = QLabel('id',self.loginwindow)
        labelid.move(20,15)

        labelpw = QLabel('pw',self.loginwindow)
        labelpw.move(18,45)

        loguserid = QLineEdit(self.loginwindow)
        loguserid.move(50, 10)
        loguserid.resize(140,20)

        loguserpw = QLineEdit(self.loginwindow)
        loguserpw.move(50, 40)
        loguserpw.resize(140,20)

        logintest = QPushButton('OK',self.loginwindow)
        logintest.move(50,70)
        logintest.resize(65,20)

        logincancle = QPushButton('close',self.loginwindow)
        logincancle.move(120,70)
        logincancle.resize(65,20)

        self.adminwindow = QDialog()

        adstuff = QTextBrowser(self.adminwindow)
        adstuff.move(10,10)
        adstuff.resize(280,380)
        adstuff.setPlainText('test')

        self.app =QApplication([])


        self.login.clicked.connect(self.chout)
        self.starbt.clicked.connect(self.start)
        self.stopbt.clicked.connect(self.stop)
        self.count.clicked.connect(self.countrun)
        '''self.admin.clicked.connect(self.adminlog)'''
        self.app.aboutToQuit.connect(self.onExit)

        logintest.clicked.connect(self.logincheck)
        logincancle.clicked.connect(self.windowclose)

    def countrun(self):
        self.bill.clear()
        grabbed, frame = cap.read()
        file = 'bill.jpg'
        cv2.imwrite(file,frame)
        th = threading.Thread(target=self.billcount)
        th.start()

    def billcount(self):
        '''self.bill.append('상품 : cho 가격 : 1500')'''
        opt = uidetect.parse_opt()
        cur_list=uidetect.main(opt)
        for i in cur_list:
            text = "상품 : " + i
            self.bill.append(text)
        os.remove('bill.jpg')

    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def run(self):
        global running
        global cap
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
        global log
        if log:
            log = False
            self.login.setText('login')
            self.user.setText('User : ')
        else:
            log = True

            self.user.setText('User : test')

            self.login.setText('logout')
            self.loginwindow.setWindowTitle('test_login')
            self.loginwindow.setWindowModality(Qt.ApplicationModal)
            self.loginwindow.resize(200, 100)
            self.loginwindow.show()

    def adminlog(self):
        self.adminwindow.setWindowTitle('adminwindow')
        self.adminwindow.setWindowModality(Qt.ApplicationModal)
        self.adminwindow.resize(300, 400)
        self.adminwindow.show()

    def logincheck(self):
        if log:
            print('login')
            self.loginwindow.close()
        else :
            print('error')

    def windowclose(self):
        self.loginwindow.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
