import cv2
import threading
import sys
import subprocess
import uidetect
import os
import shutil
import addwindow
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

running = False
log = False
billb = 0
res = 0
cuacc=0.8
billresult = []
cur_list=[]
cur_list1=[]
cur_list2=[]
cur_list3=[]
appswitch = 1

index=[] # 상품과 가격 추적하기 위해 존재
list=['pho','moch', 'che', 'songi', 'margaret', 'parkkas', 'skittles', 'hom', 'sun','oni','Ghana','ppa','cho','Miz']
list_see=['포카칩','초코모찌','치즈케이크','초코송이','마가렛','바카스맛 젤리','스키틀즈','홈럼볼','썬칩','어니언링','가나','박스형','test','test1']
price=[1500,3000,2500,1500,1000,2000,1500,1500,1000,2000,1000,1500,100,100]

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.bill = QTextBrowser(self)
        self.bill.move(880,10)
        self.bill.resize(260,330)
        self.bill.setFontPointSize(16)
        self.bill.setPlainText('물품 나오는곳')
        self.bill.setStyleSheet("background-color: #FFFFFF;")

        self.billresult = QTextBrowser(self)
        self.billresult.move(880,340)
        self.billresult.resize(260,40)
        self.billresult.setFontPointSize(16)
        self.billresult.setText('총합')
        self.billresult.setStyleSheet("background-color: #FFFFFF;")

        self.label1 = QLabel(self)
        self.label1.move(10,10)

        self.user = QLabel(self)
        self.user.move(500,520)
        self.user.setText('User :                         ')

        self.starbt = QPushButton('on', self)
        self.starbt.move(10,510)
        self.starbt.resize(80,30)
        #self.starbt.setStyleSheet("background-color: #D8FFC6;")

        self.stopbt = QPushButton('stop', self)
        self.stopbt.move(100,510)
        self.stopbt.resize(80,30)
        #self.stopbt.setStyleSheet("background-color: #D8FFC6;")

        self.accdbt = QPushButton('down', self)
        self.accdbt.move(190, 510)
        self.accdbt.resize(80, 30)

        self.accubt = QPushButton('up', self)
        self.accubt.move(280, 510)
        self.accubt.resize(80, 30)

        self.acclook = QLabel(self)
        self.acclook.move(370, 520)
        self.acclook.setText('0.9')

        '''self.admin = QPushButton('admin', self)
        self.admin.move(190, 510)
        self.admin.resize(80, 30)'''

        self.count = QPushButton('계산하기', self)
        self.count.setFont(QtGui.QFont("",20))
        self.count.setStyleSheet("background-color: #D8FFC6;")
        self.count.move(880,440)
        self.count.resize(260,100)

        self.addselfb = QPushButton('추가하기', self)
        self.addselfb.move(1010,385)
        self.addselfb.resize(130,50)
        #self.addselfb.setEnabled(False)
        self.addselfb.setStyleSheet("background-color: #F0FFFF;")#D8FFC6

        self.login = QPushButton('로그인', self)
        self.login.setStyleSheet("background-color: #F0FFFF;")#F0FFFF
        self.login.move(880,385)
        self.login.resize(130,50)

        self.setWindowTitle('testing')
        self.setGeometry(300, 300, 1150, 550)
        self.show()

        self.joinwindow = QDialog()

        labelname = QLabel('name', self.joinwindow)
        labelname.move(10, 15)

        labeljoid = QLabel('id', self.joinwindow)
        labeljoid.move(18, 45)

        labeljopw = QLabel('pw', self.joinwindow)
        labeljopw.move(16, 75)

        loguserid = QLineEdit(self.joinwindow)
        loguserid.move(50, 40)
        loguserid.resize(135, 20)

        logusername = QLineEdit(self.joinwindow)
        logusername.move(50, 10)
        logusername.resize(135, 20)

        loguserpw = QLineEdit(self.joinwindow)
        loguserpw.move(50, 70)
        loguserpw.resize(135, 20)

        jointest = QPushButton('OK', self.joinwindow)
        jointest.move(50, 100)
        jointest.resize(65, 20)

        joincancle = QPushButton('close', self.joinwindow)
        joincancle.move(120, 100)
        joincancle.resize(65, 20)

        self.loginwindow = QDialog()

        labelid = QLabel('id',self.loginwindow)
        labelid.move(20,15)

        labelpw = QLabel('pw',self.loginwindow)
        labelpw.move(18,45)

        joinbt = QPushButton('회원가입', self.loginwindow)
        joinbt.move(50, 65)
        joinbt.resize(140, 20)

        self.loginwindow.loguserid = QLineEdit(self.loginwindow)
        self.loginwindow.loguserid.move(50, 10)
        self.loginwindow.loguserid.resize(140,20)

        self.loginwindow.loguserpw = QLineEdit(self.loginwindow)
        self.loginwindow.loguserpw.setEchoMode(QLineEdit.Password)
        self.loginwindow.loguserpw.move(50, 40)
        self.loginwindow.loguserpw.resize(140,20)

        logintest = QPushButton('OK',self.loginwindow)
        logintest.move(50,90)
        logintest.resize(65,20)

        logincancle = QPushButton('close',self.loginwindow)
        logincancle.move(120,90)
        logincancle.resize(65,20)

        self.lowaccwindow = QDialog()

        labelhelp = QLabel('          로고가 잘 안보이는 제품이 있습니다.\n카메라에 제품의 로고가 보이게 재배치가 필요함니다.', self.lowaccwindow)
        labelhelp.move(20,20)

        accok = QPushButton('OK',self.lowaccwindow)
        accok.move(130,50)
        accok.resize(65,20)

        self.billselfwindow = QDialog()

        phoob = QPushButton('포카칩', self.billselfwindow)
        phoob.move(20, 20)

        mocob = QPushButton('초코모찌', self.billselfwindow)
        mocob.move(110, 20)

        cheob = QPushButton('치즈케잌', self.billselfwindow)
        cheob.move(20, 50)

        snoob = QPushButton('초코송이', self.billselfwindow)
        snoob.move(110, 50)

        marob = QPushButton('마가렛', self.billselfwindow)
        marob.move(20, 80)

        parob = QPushButton('바카스맛 젤리', self.billselfwindow)
        parob.move(290, 80)

        skiob = QPushButton('스키틀즈', self.billselfwindow)
        skiob.move(200, 20)

        homob = QPushButton('홈럼볼', self.billselfwindow)
        homob.move(290, 20)

        sunob = QPushButton('썬칩', self.billselfwindow)
        sunob.move(200, 50)

        oniob = QPushButton('어니언링', self.billselfwindow)
        oniob.move(290, 50)

        ghaob = QPushButton('가나', self.billselfwindow)
        ghaob.move(200, 80)

        ppaob = QPushButton('빠다코코낫', self.billselfwindow)
        ppaob.move(110, 80)

        self.billselfwindow.okob = QPushButton('추가하기', self.billselfwindow)
        self.billselfwindow.okob.move(20,110)
        self.billselfwindow.okob.setEnabled(False)

        self.billselfwindow.cancleob = QPushButton('삭제하기', self.billselfwindow)
        self.billselfwindow.cancleob.move(110,110)

        '''iniob = QPushButton('초기화', self.billselfwindow)
        iniob.move(200,110)'''

        exitob = QPushButton('나가기', self.billselfwindow)
        exitob.move(290,110)



        self.adminwindow = QDialog()

        adstuff = QTextBrowser(self.adminwindow)
        adstuff.move(10,10)
        adstuff.resize(280,380)
        adstuff.setPlainText('test')

        self.paywindow = QDialog()

        adpay = QTextBrowser(self.paywindow)
        adpay.move(10,10)
        adpay.resize(280,380)
        adpay.setPlainText('결제되었습니다')

        self.app =QApplication([])


        self.login.clicked.connect(self.chout)
        self.starbt.clicked.connect(self.start)
        self.stopbt.clicked.connect(self.stop)
        self.count.clicked.connect(self.countrun)
        '''self.admin.clicked.connect(self.adminlog)'''
        self.app.aboutToQuit.connect(self.onExit)
        self.addselfb.clicked.connect(self.addself)
        self.accubt.clicked.connect(self.accup)
        self.accdbt.clicked.connect(self.accdown)

        phoob.clicked.connect(self.appendpho)
        mocob.clicked.connect(self.appendmoc)
        cheob.clicked.connect(self.appendche)
        snoob.clicked.connect(self.appendsno)
        marob.clicked.connect(self.appendmar)
        parob.clicked.connect(self.appendpar)
        skiob.clicked.connect(self.appendski)
        homob.clicked.connect(self.appendhom)
        sunob.clicked.connect(self.appendsun)
        oniob.clicked.connect(self.appendoni)
        ghaob.clicked.connect(self.appendgha)
        ppaob.clicked.connect(self.appendppa)
        self.billselfwindow.okob.clicked.connect(self.appendresult)
        self.billselfwindow.cancleob.clicked.connect(self.delresult)
        #iniob.clicked.connect(self.iniresult)
        exitob.clicked.connect(self.appwindowclose)


        logintest.clicked.connect(self.logincheck)
        joinbt.clicked.connect(self.join)

        logincancle.clicked.connect(self.windowclose)
        accok.clicked.connect(self.lowwindowclose)


    def countrun(self):
        global billb
        global list
        global list_see
        global res
        global billresult
        global cur_list
        global cur_list1
        global cur_list2
        global cur_list3
        global log
        global running
        global cuacc
        acc = 0
        res = 0
        if running == True:
            if billb < 2:
                res = 0
                billresult=[]
                self.bill.clear()
                self.billresult.clear()
                grabbed, frame = cap.read()
                file = 'bill.jpg'
                cv2.imwrite(file,frame)
                opt = uidetect.parse_opt()
                cur_list3, cur_list2, cur_list, cur_list1 = uidetect.main(opt)
                print('f')
                if len(cur_list1) == 0:
                    acc = 2
                for i in cur_list2:
                    if i != -1:
                        if 0.1 < i < cuacc:
                            acc = 1
                            for j in cur_list1:
                                if cur_list3[cur_list2.index(i)] == j:
                                    cur_list[cur_list1.index(j)] -=1
                for i in cur_list1:
                    for j in list:
                        if i == j:
                            text = list_see[list.index(j)] + " " + str(price[list.index(j)]) + "원"
                            billresult.append(text)
                for i in cur_list1:
                    for j in list:
                        if i == j:
                            res += (price[list.index(j)]*cur_list[cur_list1.index(i)])
                self.bill.clear()
                self.billresult.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)])+"개")
                self.billresult.append('계 : ' + str(res) + '원')
                if acc == 0:
                    billb = 4
                    self.count.setText('결제하기')
                else:
                    self.lowaccwindow.setWindowTitle('test_lowacc')
                    self.lowaccwindow.setWindowModality(Qt.ApplicationModal)
                    self.lowaccwindow.resize(320, 70)
                    self.lowaccwindow.show()
                    billb = billb + 1
                    if billb >= 2:
                        self.addselfb.setEnabled(True)
                        self.count.setEnabled(False)
                #shutil.rmtree('runs/detect/exp')
                #os.remove('bill.jpg')
            elif billb == 4:
                self.bill.clear()
                self.billresult.clear()
                self.paywindow.setWindowTitle('test_pay')
                self.paywindow.setWindowModality(Qt.ApplicationModal)
                self.paywindow.resize(200, 100)
                self.paywindow.show()
                self.count.setText('계산하기')
                billb = 0
                cur_list=[]
                cur_list1=[]
                cur_list2=[]
                self.bill.setPlainText('물품 나오는곳')
                self.billresult.setText('총합')
                self.addselfb.setEnabled(False)
                if log == True:
                    th = threading.Thread(target=self.chout)
                    th.start()
            else:
                print('error')
                self.count.setText('계산하기')
                billb = 0
        else:
            print('error')

    def addself(self):
        global billb
        self.billselfwindow.setWindowTitle('test_billself')
        self.billselfwindow.setWindowModality(Qt.ApplicationModal)
        self.billselfwindow.resize(400, 140)
        self.billselfwindow.show()
        self.count.setText('결제하기')
        self.count.setEnabled(True)
        billb = 4

    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def accup(self):
        global cuacc
        cuacc = cuacc + 0.1
        if cuacc > 1:
            cuacc = 1
        self.acclook.setText(str(cuacc))

    def accdown(self):
        global cuacc
        cuacc = cuacc - 0.1
        if cuacc < 0.5:
            cuacc = 0.5
        self.acclook.setText(str(cuacc))

    def run(self):
        global running
        global cap
        cap = cv2.VideoCapture(2)
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
                p = pixmap.scaled(852, 480, QtCore.Qt.IgnoreAspectRatio)
                self.label1.resize(852, 480)
                self.label1.setPixmap(p)
            else:
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")
        self.label1.resize(1, 1)

    def stop(self):
        global running
        running = False
        print("stoped..")

    def join(self):
        self.joinwindow.setWindowTitle('test_join')
        self.joinwindow.setWindowModality(Qt.ApplicationModal)
        self.joinwindow.resize(200, 140)
        self.joinwindow.show()


    def onExit(self):
        print("exit")
        self.stop()

    def chout(self):
        global log
        if log:
            log = False
            self.login.setText('로그인')
            self.user.setText('User : ')
        else:
            self.loginwindow.loguserid.setText('')
            self.loginwindow.loguserpw.setText('')
            self.loginwindow.setWindowTitle('test_login')
            self.loginwindow.setWindowModality(Qt.ApplicationModal)
            self.loginwindow.resize(200, 120)
            self.loginwindow.show()

    def adminlog(self):
        self.adminwindow.setWindowTitle('adminwindow')
        self.adminwindow.setWindowModality(Qt.ApplicationModal)
        self.adminwindow.resize(300, 400)
        self.adminwindow.show()

    def logincheck(self):
        global log
        print('login')
        self.user.setText('User : test')
        self.loginwindow.close()
        log = True
        self.login.setText('로그아웃')

    def windowclose(self):
        self.loginwindow.close()

    def lowwindowclose(self):
        self.lowaccwindow.close()

    def appendpho(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'pho' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('pho')]=cur_list[cur_list1.index('pho')]+1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('pho')] > 0:
                    cur_list[cur_list1.index('pho')] = cur_list[cur_list1.index('pho')] -1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('pho')] + " " + str(price[list.index('pho')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('pho')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendmoc(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'moch' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('moch')] = cur_list[cur_list1.index('moch')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('moch')] > 0:
                    cur_list[cur_list1.index('moch')] = cur_list[cur_list1.index('moch')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('moch')] + " " + str(price[list.index('moch')]) + "원"
                print(text)
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('moch')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendche(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'che' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('che')] = cur_list[cur_list1.index('che')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('che')] > 0:
                    cur_list[cur_list1.index('che')] = cur_list[cur_list1.index('che')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('che')] + " " + str(price[list.index('che')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('che')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendsno(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'songi' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('songi')] = cur_list[cur_list1.index('songi')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('songi')] > 0:
                    cur_list[cur_list1.index('songi')] = cur_list[cur_list1.index('songi')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('songi')] + " " + str(price[list.index('songi')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('songi')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendmar(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'margaret' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('margaret')] = cur_list[cur_list1.index('margaret')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('margaret')] > 0:
                    cur_list[cur_list1.index('margaret')] = cur_list[cur_list1.index('margaret')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('margaret')] + " " + str(price[list.index('margaret')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('margaret')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendpar(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'parkkas' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('parkkas')] = cur_list[cur_list1.index('parkkas')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('parkkas')] > 0:
                    cur_list[cur_list1.index('parkkas')] = cur_list[cur_list1.index('parkkas')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('parkkas')] + " " + str(price[list.index('parkkas')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('parkkas')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendski(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'skittles' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('skittles')] = cur_list[cur_list1.index('skittles')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('skittles')] > 0:
                    cur_list[cur_list1.index('skittles')] = cur_list[cur_list1.index('skittles')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('skittles')] + " " + str(price[list.index('skittles')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('skittles')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendhom(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'hom' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('hom')] = cur_list[cur_list1.index('hom')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('hom')] > 0:
                    cur_list[cur_list1.index('hom')] = cur_list[cur_list1.index('hom')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('hom')] + " " + str(price[list.index('hom')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('hom')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendsun(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'sun' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('sun')] = cur_list[cur_list1.index('sun')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('sun')] > 0:
                    cur_list[cur_list1.index('sun')] = cur_list[cur_list1.index('sun')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('sun')] + " " + str(price[list.index('sun')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('sun')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendoni(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'oni' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('oni')] = cur_list[cur_list1.index('oni')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('oni')] > 0:
                    cur_list[cur_list1.index('oni')] = cur_list[cur_list1.index('oni')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('oni')] + " " + str(price[list.index('oni')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('oni')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendgha(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'Ghana' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('Ghana')] = cur_list[cur_list1.index('Ghana')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('Ghana')] > 0:
                    cur_list[cur_list1.index('Ghana')] = cur_list[cur_list1.index('Ghana')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('Ghana')] + " " + str(price[list.index('Ghana')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('Ghana')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendppa(self):
        global appswitch
        global res
        global cur_list
        global cur_list1
        global billresult
        global list
        global list_see
        global price
        if 'ppa' in cur_list1:
            if appswitch == 1:
                cur_list[cur_list1.index('ppa')] = cur_list[cur_list1.index('ppa')] + 1
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            else:
                if cur_list[cur_list1.index('ppa')] > 0:
                    cur_list[cur_list1.index('ppa')] = cur_list[cur_list1.index('ppa')] - 1
                    self.bill.clear()
                    for i in billresult:
                        if cur_list[billresult.index(i)] > 0:
                            self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                    res = res - 1500
                    self.billresult.clear()
                    self.billresult.append('계 : ' + str(res) + '원')
        else:
            if appswitch == 1:
                text = list_see[list.index('ppa')] + " " + str(price[list.index('ppa')]) + "원"
                billresult.append(text)
                cur_list.append(1)
                cur_list1.append('ppa')
                self.bill.clear()
                for i in billresult:
                    if cur_list[billresult.index(i)] > 0:
                        self.bill.append(i + str(cur_list[billresult.index(i)]) + "개")
                res = res + 1500
                self.billresult.clear()
                self.billresult.append('계 : ' + str(res) + '원')
            if appswitch == 0:
                print('틀린조작임니다')

    def appendresult(self):
        global appswitch
        appswitch = 1
        print(appswitch)
        self.billselfwindow.okob.setEnabled(False)
        self.billselfwindow.cancleob.setEnabled(True)

    def delresult(self):
        global appswitch
        appswitch = 0
        print(appswitch)
        self.billselfwindow.okob.setEnabled(True)
        self.billselfwindow.cancleob.setEnabled(False)

    '''def iniresult(self):
        print('ini')'''

    def appwindowclose(self):
        self.billselfwindow.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
