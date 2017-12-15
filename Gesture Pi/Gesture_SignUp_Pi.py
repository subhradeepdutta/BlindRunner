"""

This file presents the geometry/gui elements of Gesture Signup page for Gesture Pi.

PyQt5 library is used for generating the GUI for Gesture Signup page.

Created by: PyQt5 UI code generator 5.4.1

"""

# Importing PyQT5 modules
from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as paho
import os
import ssl
import json
import Gesture_LogIn
import Images_rc

class SignUp_Dialog(object):
    """Utility which creates a text boxes for sign up details like Name, Password and Email-Id.

    Once the details are entered, details are stored in AWS dynamodb.
    """

    # Define insertData function to store the entered details in DynamoDB
    def insertData(self):
        username = self.username_edit.text()
        email = self.password_edit_2.text()
        password = self.password_edit.text()

        params = {
            "username": username,
            "password": password,
            "email-id": email
        }

        msg = json.dumps(params)
        self.mqttc.publish("login_details", msg,qos=1)
        
        self.loginWindow = QtWidgets.QDialog()
        self.login = Gesture_LogIn.Login_Dialog()
        self.login.setupUi(self.loginWindow)
        self.loginWindow.show()
        self.mqttc.loop_stop()
        self.obj.destroy()
        
    
    def setupUi(self, Dialog):
        """Setting up the Gesture Signup page for storing authentication details in dynamodb.

        Args:
            QtDialog window object

        SignUp button is provided to capture the image and to send the image to AWS Rekognition.
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.obj = Dialog
        Dialog.setStyleSheet("QDialog{Border-Image: url(:/Images/f1.jpg)}")
        self.username_edit = QtWidgets.QLineEdit(Dialog)
        self.username_edit.setGeometry(QtCore.QRect(610, 290, 221, 41))
        self.username_edit.setObjectName("username_edit")
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(490, 510, 191, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.login_button.setObjectName("login_button")
        self.password_label = QtWidgets.QLabel(Dialog)
        self.password_label.setGeometry(QtCore.QRect(370, 360, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.password_label.setFont(font)
        self.password_label.setStyleSheet("color: rgba(255,255,255,200);")
        self.password_label.setObjectName("password_label")
        self.password_edit = QtWidgets.QLineEdit(Dialog)
        self.password_edit.setGeometry(QtCore.QRect(610, 360, 221, 41))
        self.password_edit.setObjectName("password_edit")
        self.username_label = QtWidgets.QLabel(Dialog)
        self.username_label.setGeometry(QtCore.QRect(370, 290, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.username_label.setFont(font)
        self.username_label.setStyleSheet("color: rgba(255,255,255,200);")
        self.username_label.setObjectName("username_label")
        self.password_label_2 = QtWidgets.QLabel(Dialog)
        self.password_label_2.setGeometry(QtCore.QRect(370, 430, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.password_label_2.setFont(font)
        self.password_label_2.setStyleSheet("color: rgba(255,255,255,200);")
        self.password_label_2.setObjectName("password_label_2")
        self.password_edit_2 = QtWidgets.QLineEdit(Dialog)
        self.password_edit_2.setGeometry(QtCore.QRect(610, 430, 221, 41))
        self.password_edit_2.setObjectName("password_edit_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(390, 130, 451, 91))
        font = QtGui.QFont()
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255)); background-color: rgba(100,100,100, 100);")
        self.label.setObjectName("label")

        # Button event for login_button
        self.login_button.clicked.connect(self.insertData)
        

        # AWS MQTT configuration settings
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "UiPi"
        thingName = "UiPi"
        caPath = "aws-iot-rootCA.crt"
        certPath = "cert.pem"
        keyPath = "privkey.pem"

        # Define on_connect function to subscribe to topic
        def on_connect(client, userdata, flags, rc):
            global connflag
            connflag = True
            print("Connection returned result: " + str(rc) )
            print("\n")
            client.subscribe("#" , 1 )

        # Define on_message function to listen to notifications from AWS
        def on_message(client, userdata, msg):
            global piMode
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
            print("\n")

        # Declaring MQTT interfaces
        self.mqttc = paho.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message


        # Starting the MQTT connection
        self.mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.mqttc.connect(awshost, awsport, keepalive=60)
        self.mqttc.loop_start()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # Define retranslateUi funtion to change the text to different language.
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.login_button.setText(_translate("Dialog", "Sign Up"))
        self.password_label.setText(_translate("Dialog", "PASSWORD"))
        self.username_label.setText(_translate("Dialog", "USERNAME"))
        self.password_label_2.setText(_translate("Dialog", "EMAIL-ID"))
        self.label.setText(_translate("Dialog", "Create Account"))


# The main function will create a QApplication for QDialog window for diaplaying Gesture SignUp page
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

