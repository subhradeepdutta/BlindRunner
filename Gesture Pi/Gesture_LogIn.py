"""

This file presents the geometry/gui elements of Gesture_Login Pi.

PyQt5 library is used for generating the GUI for Gesture_Login Pi.

Created by: PyQt5 UI code generator 5.4.1

"""

# Importing modules for Camera, PyQt5, time etc.,
from PyQt5 import QtCore, QtGui, QtWidgets
import Gesture_SignUp_Pi
import Gesture_Logic
import paho.mqtt.client as paho
import os
import ssl
import json
import time
from time import sleep

# Global variables section
mqttc = None

class ThreadClass(QtCore.QThread):
    """Utility which creates a thread to continously capture images from camera.

    This utility triggers a signal for 0.1 seconds to display the image on the
    Videographics window.
    """
    
    trigger = QtCore.pyqtSignal(['QString'])
    def __init__(self,parent = None):
        super(ThreadClass,self).__init__(parent)
        
        
    def run(self):
        
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "UiPi"
        thingName = "UiPi"
        caPath = "aws-iot-rootCA.crt"
        certPath = "cert.pem"
        keyPath = "privkey.pem"

        def on_connect(client, userdata, flags, rc):
            global connflag
            connflag = True
            print("Connection returned result: " + str(rc) )
            client.subscribe("LoginCheckResult",1)
                
        def on_message(client, userdata, msg):
            global piMode
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
            if(msg.topic == "LoginCheckResult"):
                if(str(msg.payload.decode("utf-8")) == "LoginSuccessful"):
                    print("User Found ! ")
                    self.trigger.emit('Valid Username And Password')
                    
                else:
                    print("User Not Found !")
                    self.trigger.emit('Invalid Username And Password')
                    
                    

        global mqttc
        mqttc = paho.Client()
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message



        mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        mqttc.connect(awshost, awsport, keepalive=60)

        mqttc.loop_start()
        

class Login_Dialog(object):
    def showMessageBox(self,message):
        global mqttc
        if(message == 'Invalid Username And Password'):
            self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.msgBox.setWindowTitle("Warning")
            self.msgBox.setText(message)
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msgBox.show()
        else:
            self.loginWindow = QtWidgets.QDialog()
            self.prog = Gesture_Logic.UIProgram(self.loginWindow)
            self.loginWindow.show()
            mqttc.loop_stop()
            self.obj.destroy()
            
       
        
        
    def signUpShow(self):
        global mqttc
        self.signUpWindow = QtWidgets.QDialog()
        self.ui = Gesture_SignUp_Pi.SignUp_Dialog()
        self.ui.setupUi(self.signUpWindow)
        self.signUpWindow.show()
        mqttc.loop_stop()
        self.obj.destroy()
       
        
    def loginCheck(self):
        username_local = self.username_edit.text()
        password_local = self.password_edit.text()

        params = {
            "username": username_local,
            "password": password_local
        }

        msg = json.dumps(params)
        print(msg)
        global mqttc
        mqttc.publish("LoginCheck", msg,qos=1)

        
        
    def signUpCheck(self):
        print(" Sign Up Button Clicked !")
        self.signUpShow()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setStyleSheet("QDialog {border-image: url(:/Images/f1.jpg)}")
        Dialog.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        Dialog.setModal(False)
        self.obj = Dialog
        self.msgBox = QtWidgets.QMessageBox()
        self.username_SignInText = QtWidgets.QLabel(Dialog)
        self.username_SignInText.setGeometry(QtCore.QRect(360, 370, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.username_SignInText.setFont(font)
        self.username_SignInText.setStyleSheet("color: rgba(255,255,255,200);")
        self.username_SignInText.setObjectName("username_SignInText")
        self.password_SignInText = QtWidgets.QLabel(Dialog)
        self.password_SignInText.setGeometry(QtCore.QRect(360, 439, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.password_SignInText.setFont(font)
        self.password_SignInText.setStyleSheet("color: rgba(255,255,255,200);")
        self.password_SignInText.setObjectName("password_SignInText")
        self.username_edit = QtWidgets.QLineEdit(Dialog)
        self.username_edit.setGeometry(QtCore.QRect(610, 370, 221, 41))
        self.username_edit.setObjectName("username_edit")
        self.password_edit = QtWidgets.QLineEdit(Dialog)
        self.password_edit.setGeometry(QtCore.QRect(610, 440, 221, 41))
        self.password_edit.setObjectName("password_edit")
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(360, 520, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.login_button.setObjectName("login_button")
        self.signup_button = QtWidgets.QPushButton(Dialog)
        self.signup_button.setGeometry(QtCore.QRect(650, 520, 181, 101))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.signup_button.setFont(font)
        self.signup_button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.signup_button.setObjectName("signup_button")
        self.SignInText = QtWidgets.QLabel(Dialog)
        self.SignInText.setGeometry(QtCore.QRect(480, 240, 241, 91))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.SignInText.setFont(font)
        self.SignInText.setStyleSheet("color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255))")
        self.SignInText.setObjectName("SignInText")
        self.BlindRunnerText = QtWidgets.QLabel(Dialog)
        self.BlindRunnerText.setGeometry(QtCore.QRect(200, 50, 781, 141))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.BlindRunnerText.setFont(font)
        self.BlindRunnerText.setStyleSheet("background-color: rgba(100,100,100, 100);color: rgba(255,255,255,200);")
        self.BlindRunnerText.setObjectName("BlindRunnerText")
        self.SridharText = QtWidgets.QLabel(Dialog)
        self.SridharText.setGeometry(QtCore.QRect(390, 740, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SridharText.setFont(font)
        self.SridharText.setStyleSheet("color: rgba(255,255,255,200);")
        self.SridharText.setObjectName("SridharText")
        self.SharatText = QtWidgets.QLabel(Dialog)
        self.SharatText.setGeometry(QtCore.QRect(10, 740, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SharatText.setFont(font)
        self.SharatText.setStyleSheet("color: rgba(255,255,255,200);")
        self.SharatText.setObjectName("SharatText")
        self.Subhradeeptext = QtWidgets.QLabel(Dialog)
        self.Subhradeeptext.setGeometry(QtCore.QRect(870, 740, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Subhradeeptext.setFont(font)
        self.Subhradeeptext.setStyleSheet("color: rgba(255,255,255,200);")
        self.Subhradeeptext.setObjectName("Subhradeeptext")
		
		######################### Button Event ##############################
        self.login_button.clicked.connect(self.loginCheck)
        self.signup_button.clicked.connect(self.signUpCheck)
        #####################################################################
        
        self.threadclass = ThreadClass()
        self.threadclass.trigger.connect(self.showMessageBox)
        self.threadclass.start()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.username_SignInText.setText(_translate("Dialog", "USERNAME"))
        self.password_SignInText.setText(_translate("Dialog", "PASSWORD"))
        self.login_button.setText(_translate("Dialog", "Login"))
        self.signup_button.setText(_translate("Dialog", "Sign Up"))
        self.SignInText.setText(_translate("Dialog", "SIGN IN"))
        self.BlindRunnerText.setText(_translate("Dialog", "The Blind Runner"))
        self.SridharText.setText(_translate("Dialog", "Sridhar Pavithrapu"))
        self.SharatText.setText(_translate("Dialog", "Sharat RP"))
        self.Subhradeeptext.setText(_translate("Dialog", "Subhradeep Dutta"))

import Images_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Login_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

