import numpy as np
import urllib
from urllib import request
import cv2
import sqlite3
from gtts import gTTS
from playsound import playsound
from PyQt5 import QtCore, QtGui, QtWidgets
from forex_python.converter import CurrencyRates

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(720, 550)
        Form.setMinimumSize(QtCore.QSize(720, 550))
        Form.setMaximumSize(QtCore.QSize(720, 550))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Downloads/Res/logotitle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setWindowOpacity(1.0)
        Form.setStyleSheet("background-image: url(:/newPrefix/Background.png);\n"
"font: 25 8pt \"Microsoft YaHei Light\";")
        self.capture = QtWidgets.QPushButton(Form)
        self.capture.setGeometry(QtCore.QRect(90, 220, 111, 41))
        self.capture.setStyleSheet("#Download{\n"
"background-color: rgb(21, 131, 212);\n"
"border: 1px solid gray;\n"
"border-radius: 2px;\n"
"}\n"
"#Download:pressed{\n"
"background-color: rgb(21, 133, 214);\n"
"    border-color: rgb(20, 123, 199);\n"
"}")
        self.capture.setObjectName("capture")
        self.Browse = QtWidgets.QPushButton(Form)
        self.Browse.setGeometry(QtCore.QRect(90, 310, 101, 51))
        self.Browse.setStyleSheet("#Browse{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"}\n"
"#Browse:pressed{\n"
"border-color: rgb(255, 255, 255);\n"
"}")
        self.Browse.setObjectName("Browse")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(380, 170, 141, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(380, 280, 141, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(380, 400, 141, 21))
        self.label_5.setObjectName("label_5")
        self.cur_out = QtWidgets.QTextEdit(Form)
        self.cur_out.setGeometry(QtCore.QRect(390, 210, 241, 41))
        self.cur_out.setObjectName("cur_out")
        self.coun_out = QtWidgets.QTextEdit(Form)
        self.coun_out.setGeometry(QtCore.QRect(390, 320, 241, 41))
        self.coun_out.setObjectName("coun_out")
        self.inr = QtWidgets.QTextEdit(Form)
        self.inr.setGeometry(QtCore.QRect(390, 440, 241, 41))
        self.inr.setObjectName("inr")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.capture.clicked.connect(self.fn)
        ##self.Browse.clicked.connect(self.brow)
   ## def brow(self):

    def fn(self):

        img_counter = 0
        url = "http://192.168.43.85:8080/shot.jpg?rnd=147162"

        while True:
            imgResp = urllib.request.urlopen(url)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            cv2.imshow("test", img)
            k = cv2.waitKey(1)
            if k % 256 == 32:
                img_name = "image_{}.png".format(img_counter)
                cv2.imwrite(img_name, img)
                cam_input = img_name
                ##print(img_name)
                ## print ("{} written!".format(img_name))
                img_counter += 1
                break
        cv2.destroyAllWindows()

        con = sqlite3.connect('currencies.db')

        cur = con.cursor()
        s = 'SELECT image FROM currency'
        cur.execute(s)

        r = cur.fetchall()
        max = 0
        for rw in r:
            db_image = rw[0]
            ##print(db_image)

            img1 = cv2.imread(db_image)
            img2 = cv2.imread(cam_input)

            orb = cv2.ORB_create()

            kp1, des1 = orb.detectAndCompute(img1, None)
            kp2, des2 = orb.detectAndCompute(img2, None)

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matches = bf.match(des1, des2)
            matches = sorted(matches, key=lambda x: x.distance)
            c = 0
            for m in matches:
                ##print(m.distance)
                if (m.distance) < 50.0:
                    c = c + 1

            if c > max:
                max = c
                cur.execute("SELECT cur_name,country,type,no FROM currency WHERE image=?", (db_image,))
                y = cur.fetchall()
        ##print(max)
        for i in y:
            curr=(i[0])
            country=(i[1])
            cur_index=(i[2])
            bbc=(i[3])
        speech = gTTS(country+curr)
        speech.save("hello.mp3")
        playsound('C:/Users/nagar/Desktop/b10/hello.mp3')
        self.cur_out.setText(curr)
        self.coun_out.setText(country)
        co = CurrencyRates()
        ##print(cur_index)
        ##print(bbc)
        abc=co.convert(cur_index, 'INR',bbc)
        self.inr.setText(str(abc))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Kryptor"))
        self.capture.setText(_translate("Form", "CAPTURE"))
        self.Browse.setText(_translate("Form", "Browse"))
        self.label_3.setText(_translate("Form", "CURRENCY NAME"))
        self.label_4.setText(_translate("Form", "COUNTRY"))
        self.label_5.setText(_translate("Form", "INR VALUE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

